import logging
import subprocess
import codecs
import dataclasses


def set_up_logging(level, out_file):
    num_level = getattr(logging, level.upper(), None)
    if not isinstance(num_level, int):
        raise ValueError("Invalid log level: {}".format(level))
    handlers = []
    handlers.append(logging.StreamHandler())
    handlers.append(logging.FileHandler(filename=out_file, encoding="utf8"))
    logging.basicConfig(level=num_level, handlers=handlers,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@dataclasses.dataclass
class CommitInfo:
    hash: str
    clean_worktree: bool


def get_git_info():
    logger = logging.getLogger("envinfo")
    try:
        commit_id_out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True)
        commit_id = codecs.decode(commit_id_out.stdout).strip()
        clean_tree_out = subprocess.run(["git", "status", "--porcelain"], capture_output=True)
        clean_worktree = len(clean_tree_out.stdout) == 0
        return CommitInfo(hash=commit_id, clean_worktree=clean_worktree)
        logger.debug("Running on commit {} ({} worktree)".format(commit_id,
                                                                 "clean" if clean_worktree else "dirty"))
    except Exception:
        return None
        logger.exception("Failed to get information on git status")
