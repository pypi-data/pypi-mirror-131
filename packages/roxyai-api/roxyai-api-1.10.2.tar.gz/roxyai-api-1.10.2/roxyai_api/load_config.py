# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
import sys
import os
from pathlib import Path
import json5 as json
import re
from termcolor import cprint

import logging.config
log = logging.getLogger(__name__)


class BaseConfig():
    _path = None
    _items = {}

    def __init__(self, src: dict):
        self._items = {}
        self.update(src)

    def update(self, src: dict):
        """ 設定値の内容を辞書から更新
        Args:
            src (dict):     値を読み込む辞書
        """
        for key in src.keys():
            if key in dir(self):
                if (
                    # 定数や内部変数、メソッドなら無視する
                    key[0] == "_"
                    or key.isupper()
                    or callable(getattr(self, key))
                ):
                    continue

                val = src[key]
                setattr(self, key, val)
                self._items[key] = val
                # print(f'>>>>>>>>> self: {self}, attr: {key}, val: {val}')

    @classmethod
    def load(cls, path: Path):
        """ 行コメントを含むJSONファイルの読み込み
        Args:
            path (str)      JSON形式の設定ファイルパス
        Returns:
            dict            読み込んだ設定ファイルの辞書
        """
        path = Path(path)
        if not path.exists():
            raise RuntimeError(
                f'not found configuration file: {path.resolve().as_posix()}'
            )
        try:
            data = path.read_text(encoding="utf_8")
            dic = json.loads(data)
            instance = cls(dic)
            instance._path = path.absolute().resolve()
        except Exception as e:
            raise RuntimeError(
                f'failed to load configuration file: {path.resolve().as_posix()}\n{e}'
            )
        return instance

    @property
    def items(self):
        """ 設定ファイル情報の一覧取得
        """
        return self._items

    @property
    def path(self):
        """ 設定ファイルのパス
        """
        return self._path

    def dump_items(
        self, dumper, prefix: str, max_length: int = 255, default=True, exclusion=[]
    ):
        """ ユーザが設定したデータの一覧をログ出力
        """
        if default:
            # デフォルト値を含む場合
            base_attrs = dir(super())
            items = {
                attr: getattr(self, attr) for attr in dir(self)
                if (
                    attr not in base_attrs
                    and attr[:1].islower()
                    and not callable(getattr(self, attr))
                    and attr not in ('path', 'items')
                )
            }

        else:
            items = self._items

        for name, val in items.items():
            if name in exclusion:
                # 除外のキーは除く
                continue
            text = f'{prefix}{name:25}: {val}'
            if len(text) >= max_length - 3:
                text = text[:(max_length - 3)] + '...'
            dumper(text)

    def __str__(self):
        name = self.__class__.__name__.replace('Config', '')
        text = f'{name} : {self._path}'
        return text


class CommonConfig(BaseConfig):
    """ 共通設定ファイル
    """
    # 定数定義
    DEFAULT_PATH = (Path(__file__).parent / '../../../config/common.json').resolve()

    # デフォルト設定
    product_top = str(Path(os.environ.get('Roxy_AI', '')) / 'roxy-ai-runtime/fixed_model')

    @classmethod
    def load(cls, path=None):
        path = path or cls.DEFAULT_PATH
        if not path.exists():
            log.error(f'Config file does not exist: {path.absolute()}')
            cprint(
                f'Please copy config files "{cls.DEFAULT_PATH.name}" from default folder. '
                f'({cls.DEFAULT_PATH.parent / "default"})', color='yellow'
            )
            sys.exit(1)
        return super().load(path)


class ServerConfig(BaseConfig):
    """ 共通サーバ設定ファイル
    """
    # 定数定義
    DEFAULT_PATH = (Path(__file__).parent / '../../../config/server.json').resolve()

    @classmethod
    def load(cls, path=None):
        path = path or cls.DEFAULT_PATH
        if not path.exists():
            log.error(f'Config file does not exist: {path.absolute()}')
            cprint(
                f'Please copy config files "{cls.DEFAULT_PATH.name}" from default folder. '
                f'({cls.DEFAULT_PATH.parent / "default"})', color='yellow'
            )
            sys.exit(1)
        return super().load(path)

    def __init__(self, dic: dict):
        super().__init__(dic)
        for item, val in dic.items():
            if type(val) is list:
                hosts = []
                ports = []
                for v in val:
                    mr = re.match(r'(?P<host>(\d+\.\d+\.\d+\.\d+))\:(?P<port>(\d+))', v)
                    if mr:
                        hosts.append(mr['host'])
                        ports.append(int(mr['port']))
                setattr(self, item + '_host', hosts)
                setattr(self, item + '_port', ports)
            self._items[item] = val
