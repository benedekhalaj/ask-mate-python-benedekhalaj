from werkzeug.utils import secure_filename
import os
import datetime
import bcrypt

UPLOAD_FOLDER = './static/images'


def get_data_by_id(data_list, value, id):
    for data in data_list:
        if data[value] == int(id):
            return data


def update_data_by_form(data, form):
    for key, value in form.items():
        data[key] = value
    return data


def upload_file(request_attributes, id, r_type='questions'):
    file = request_attributes.files['file']
    if file:
        filename = secure_filename(file.filename)
        filename = add_id_to_file(filename, id)
        file.save(os.path.join(f"{UPLOAD_FOLDER}/{r_type}", filename))
        return f"images/{r_type}/{filename}"
    return None


def add_id_to_file(filename, id):
    name, extension = filename.split('.')
    name = f"{name}_{id}"
    return ".".join([name, extension])


def delete_file(r_type, id):
    directory_in_str = f'{UPLOAD_FOLDER}/{r_type}'
    directory = os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(f"_{id}.png") or filename.endswith(f"_{id}.jpg"):
            os.remove(os.path.join(f"{directory_in_str}/{filename}"))


def add_submission_time():
    return datetime.datetime.now().isoformat()


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))
