import hashlib

def generate_room_code(user1, user2):
    users = sorted([user1, user2])
    unique_string = f"{users[0]}_{users[1]}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:10]