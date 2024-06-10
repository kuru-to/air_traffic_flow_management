import pydantic

from ..utils.config_util import read_config


@pydantic.dataclasses.dataclass
class OptimizationParameters:
    """開発者が設定するパラメータ群(スレッド数, 目的関数の傾斜など)
    """
    MODEL_NAME: str

    NUM_THREADS: int
    MAX_SECONDS: int

    CPLEX_LOG_FILE: str

    @classmethod
    def import_(cls, config_section: str) -> 'OptimizationParameters':
        """config ファイルから読み取る.
        読み取り対象のファイルも config から読み取り

        Args:
            config_section (str): 読み取り対象の section
        """
        config = read_config(section=config_section)
        filename_config_opt = config.get("PATH_CONFIG") + config.get("CONFIG_OPTIMIZER")
        config_opt = read_config(filename_config_opt, section=config_section)
        return cls(**config_opt)


class BusinessRuleParameters:
    """ユーザーが設定するパラメータ群
    """
    pass
