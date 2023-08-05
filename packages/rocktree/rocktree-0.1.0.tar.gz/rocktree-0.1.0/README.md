# Rocktree

A tool for making keeping your working testing tree rock solid up to date
with the latest developments in place with upstream link.

Consider giving us a :star:. Made with love by contributors.

**In development, yet to be implemented**

## Concept

So for example we have `http://example.com/testing-repo`. It gets updated
time to time and we want to keep up to date with it all the time blanking
out all the local changes as soon as the changes are pulled from
upstream. It works on the bases of [`patchutils`](https://github.com/xcodz-dot/patchutils)
which works on the bases of patchfiles, update files and directory trees.

To download from upstream for the first time you can use the `rocktree.clone(url="http://my_url.com/repo")`
after that the repo should contain a `.rocktree` file which contains the
upstream link. You can then use the method `rocktree.update_from_file(dir="local_repo")`.
You can also force update from a specified repo using the provided method
`rocktree.update(dir="local_repo", url="http://my_url.com/repo")