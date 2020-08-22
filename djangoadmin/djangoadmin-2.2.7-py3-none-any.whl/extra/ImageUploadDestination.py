import random


# Create custom path and filename to save media.
def ImageUploadDestination(instance, filename):
    if filename:
        get_extension = filename.split('.')[-1]
        get_filename = random.randint(0, 1000000000000)
        new_filename = f"IMG{get_filename}UN{instance.user.username}.{get_extension}"
        return(f'djangoadmin/{instance.user.id}_{instance.user.username}/{new_filename}')