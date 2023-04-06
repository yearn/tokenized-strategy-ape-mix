import ape


def days_to_secs(days: int) -> int:
    return 60 * 60 * 24 * days


def increase_time(chain, seconds):
    chain.pending_timestamp = chain.pending_timestamp + seconds
    chain.mine(timestamp=chain.pending_timestamp)
