# # https://psutil.readthedocs.io/en/latest/#recipes
# import os
# import psutil
# import signal
#
#
# def find_processes_by_name(name: str) -> list:
#     """Return a list of processes matching 'name'."""
#     ls = []
#     for p in psutil.process_iter(["name", "exe", "cmdline"]):
#         if name == p.info['name'] or \
#                 p.info['exe'] and os.path.basename(p.info['exe']) == name or \
#                 p.info['cmdline'] and p.info['cmdline'][0] == name:
#             ls.append(p)
#     return ls
#
#
# # def kill_process_id(proc_pid: int, recursive: bool = True):
# def kill_process_id(proc_pid: int):
#     """Kill a process ID"""
#     process = psutil.Process(proc_pid)
#     # for proc in process.children(recursive=recursive):
#     for proc in process.children(recursive=True):
#         proc.kill()
#     process.kill()
#
#
# def kill_process_tree(pid: int, sig=signal.SIGTERM, include_parent=True, timeout=None, on_terminate=None) -> tuple:
#     """
#     Kill a process tree (including grandchildren) with signal "sig" and return a (gone, still_alive) tuple.
#
#     "on_terminate", if specified, is a callback function which is called as soon as a child terminates.
#     """
#     assert pid != os.getpid(), "won't kill myself"  # nosec - skip B101:assert_used
#     parent = psutil.Process(pid)
#     children = parent.children(recursive=True)
#     if include_parent:
#         children.append(parent)
#     for p in children:
#         try:
#             p.send_signal(sig)
#         except psutil.NoSuchProcess:
#             pass
#     gone, alive = psutil.wait_procs(children, timeout=timeout,
#                                     callback=on_terminate)
#     return (gone, alive)
