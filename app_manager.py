def procedure(zk):
    zk.ensure_path("/events")
    zk.ensure_path("/results")
    