"""Calculate a hash given a username and a passwordword.
This file is actually a hardlink."""

def calculate_hash(uname, password):
    #Make hash
    hasher = SHA256.new()
    hasher.update(password)
    hasher.update(uname)
    hasher.update("I'd rather have a free bottle in front of me than a pre-frontal lobotomy.")
    hasher.update(password)
    userkey = hasher.hexdigest()
    return userkey

