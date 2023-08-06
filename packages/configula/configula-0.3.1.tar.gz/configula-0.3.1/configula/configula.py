import io
import os

from tomlkit import loads


class Configula:
    MYSQL_TYPE = ('my', 'mysql', 'maria', 'mariadb')
    POSTGRES_TYPE = ('pg', 'postgre', 'postgres', 'postgresql')

    def __init__(
        self,
        prefix,
        config_locations=None,
        config_env_var_name=None
    ):
        """
        Args:
            `config_locations` (list): a list of string file paths
                where to load configurations from
            `config_env_var_name` (str): in case `config_locations` was
                not provided, load file configurations
            from a file pointed by this environment variable
            `prefix` (str): all configurations provided by environment
                variables will be prefixed with this value

        Example:

            Configula(
                prefix='PAPERMERGE',
                config_locations=[
                    'papermerge.toml',
                    '/etc/papermerge.toml'
                ],
                config_env_var_name='PAPERMERGE_CONFIG'
            )

        In case papermerge.toml was not found in current location
        and /etc/papermerge.toml does not exists, it continue look for
        configuration file by looking at PAPERMERGE_CONFIG environment
        variable. If PAPERMERGE_CONFIG environment variable exists and is
        (for example):

            PAPERMERGE_CONFIG=/home/eugen/papermerge.toml

        will load configurations from /home/eugen/papermerge.toml. In case
        either /home/eugen/papermerge.toml does not exists or
        PAPERMERGE_CONFIG environment variable does not exists, Configula
        will silently give up searching for toml configuration file will look
        up for config values only in envrionment variables prefixed
        with 'PAPERMERGE'
        """
        self.config_locations = config_locations
        self.config_env_var_name = config_env_var_name
        self.prefix = prefix
        self._toml_config = self.load_toml()

    def _loads(self, file_path):
        with io.open(file_path, encoding="utf-8") as f:
            return loads(f.read())

    def load_toml(self):
        """
        Loads toml configuration file from self.config_locations or
        from location pointed by self.config_env_var_name.

        Returns None in case toml configuration file was not found.
        Returns a dictionary of configuration if toml config was found.
        """
        for config_file in self.config_locations:
            if os.path.exists(config_file):
                return self._loads(config_file)

        config_file = os.environ.get(self.config_env_var_name, False)
        if config_file and os.path.exists(config_file):
            return self._loads(config_file)

    def get(self, section_name, var_name, default=None):
        """
        Reads `var_name` in section `section_name` either from toml config
        or from environment variable.

        In case no value is found in above sources value provided as `default`
        will be returned.
        """
        env_name = f"{self.prefix}_{section_name}_{var_name}".upper()

        try:
            value = os.getenv(env_name) or self._toml_config[section_name][var_name]
        except Exception as exc:
            value = None

        return value or default

    def get_var(self, var_name, default=None):
        """
        Reads `var_name` either from toml config or from environment variable.

        In case no value is found in above sources value provided as `default`
        will be returned.
        """
        env_name = f"{self.prefix}_{var_name}".upper()

        try:
            value = os.getenv(env_name) or self._toml_config[var_name]
        except Exception as exc:
            value = None

        return value or default

    def get_django_databases(self, proj_root):
        """Returns dictionary for django DATABASES settings"""
        # by default, if no value is provided for database, use
        # sqlite3 with file located in `proj_root`
        section = 'database'
        result = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(
                    self.get(
                        section,
                        'dir',
                        default=proj_root
                    ),
                    'db.sqlite3'
                )
            }
        }

        if self.get(section, 'type', False) in self.POSTGRES_TYPE:
            result["default"] = {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": self.get(section, "name", "papermerge"),
                "USER": self.get(section, "user", "papermerge"),
            }
            result["default"]["PASSWORD"] = self.get(section, 'pass', "")
            result["default"]["HOST"] = self.get(
                section,
                'host',
                'localhost'
            )
            result["default"]["PORT"] = self.get(section, 'port', 5432)
        elif self.get(section, 'type', False) in self.MYSQL_TYPE:
            result['default'] = {
                "ENGINE": "django.db.backends.mysql",
                "NAME": self.get(section, 'name', 'papermerge'),
                "USER": self.get(section, 'user', 'papermerge'),
            }
            result["default"]["PASSWORD"] = self.get(section, 'pass', '')
            result["default"]["HOST"] = self.get(
                section, 'host', 'localhost'
            )
            result["default"]["PORT"] = self.get(section, 'port', 3306)

        return result

    @property
    def has_mysql(self):
        return self.get('database', 'type') in self.MYSQL_TYPE
