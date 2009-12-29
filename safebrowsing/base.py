from platform import node
import conf

class BaseDbObj(object):
    db_engine   = getattr(conf, 'DATABASE_ENGINE')
    db_name     = getattr(conf, 'DATABASE_NAME')
    db_user     = getattr(conf, 'DATABASE_USER')
    db_password = getattr(conf, 'DATABASE_PASSWORD')
    db_host     = getattr(conf, 'DATABASE_HOST', node())
    db_port     = getattr(conf, 'DATABASE_PORT')
    api_key     = getattr(conf, 'API_KEY')

    def get_version(self, badware_type):
        """To be subclassed by backends"""
        return NotImplementedError

    def insert_version_row(self, badware_type, version_number):
        """To be subclassed by backends"""
        return NotImplementedError

    def update_version_row(self, badware_type, new_version_number, version_number):
        """To be subclassed by backends"""
        return NotImplementedError

    def insert_rows(self, url_hash_dict):
        """To be subclassed by backends"""
        return NotImplementedError

    def delete_rows(self, url_hash_dict):
        """To be subclassed by backends"""
        return NotImplementedError

    def lookup_by_md5(self, md5_hash_list):
        """To be subclassed by backends"""
        return NotImplementedError
