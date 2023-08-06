import os
import time
from os import path
import threading
from typing import TextIO, Tuple
from flask import Flask, jsonify, request, send_from_directory
import patchutils
from threading import Lock
import logging
import sys

WSGIServer = None
try:
    from gevent.pywsgi import WSGIServer
except ModuleNotFoundError:
    pass

__version__ = "1.0.0"


class RockTreeServer:
    """
    use `update_interval` to specify when to update the in memory directory information from disk.
    """

    def __init__(
        self,
        directory: str = ".",
        update_interval: int = None,
        logfp: TextIO = sys.stderr,
    ):
        self.logger = logging.Logger("RockTreeServer")
        self.logger.addHandler(logging.StreamHandler(logfp))
        self.logger.debug("Initialized the logger")
        self.logger.info(f"RockTreeServer.version = {__version__}")

        self.logger.info("Creating directory information for %s", directory)
        self.dinfo = patchutils.create_info_from_directory(directory)
        self.logger.debug(self.dinfo)
        self.directory = directory
        self.update_interval = update_interval
        self.lock = Lock()
        self.logger.info("Done with directory information")

        self.logger.debug("Initalizing Flask App")
        self.app = Flask(__name__)
        self.app.route("/v1/get_patch", methods=["POST"])(self._v1_get_patch)
        self.app.route("/v1/download/<path:filename>")(self._v1_get_file)
        self.app.route("/api")(self._list_versions)
        self.logger.debug("Flask Initialized")
        self.start_scheduled_updater()

    def _list_versions(self):
        return jsonify(versions="v1")

    def _v1_get_patch(self):
        self.lock.acquire()
        self.lock.release()
        dinfo = request.json["dirinfo"]
        return jsonify(patchutils.create_patch_from_info(dinfo, self.dinfo))

    def _v1_get_file(self, filename: str):
        self.lock.acquire()
        self.lock.release()
        self.logger.info("Download requested: %s", filename)
        return send_from_directory(
            os.path.join(os.getcwd(), self.directory), filename, as_attachment=True
        )

    def _scheduled_update(self):
        if self.update_interval is None:
            self.logger.warn(
                "Scheduled updates are disabled due to update_interval being None"
            )
            return

        while True:
            time.sleep(self.update_interval)
            self.logger.info("Scheduled update triggered!")
            self.update_now()

    def start_scheduled_updater(self):
        """Spawn a scheduled updater"""
        threading.Thread(target=self._scheduled_update).start()

    def update_now(self):
        self.logger.debug("Acquiring Lock for requested update")
        with self.lock:
            self.logger.debug("Lock Acquired for requested update")
            self.logger.info("Refreshing directory information now")
            self.dinfo = patchutils.create_info_from_directory(self.directory)
            self.logger.info("Refreshed directory information complete")
        self.logger.debug("Lock Released")

    def spawn_debug_server(self, *args, **kwargs) -> bool:
        self.logger.info("Spawning Debug Server")
        self.app.run(*args, **kwargs)
        return True

    def spawn_gevent_server(self, *args, **kwargs) -> bool:
        if WSGIServer is not None:
            self.logger.info("Spawning Gevent Server")
            http_server = WSGIServer(args[0], self.app, *args[1:], **kwargs)
            http_server.serve_forever()
        else:
            self.logger.warning(
                "Gevent server not found. Please install pip package`rocktree[server-gevent]`"
            )
            return False
        return True

    def spawn_server(self, host: Tuple[str, int]) -> bool:
        if self.spawn_gevent_server(host):
            return True
        if self.spawn_debug_server(host):
            return True
        return False
