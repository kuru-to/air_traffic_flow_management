"""ファイルの処理に関する便利ツールをまとめたスクリプト"""

from __future__ import annotations

import os
import shutil
from csv import DictReader, DictWriter
from pathlib import Path
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class FileUtilException(Exception):
    pass


def create_dir_if_not_exists(dir_name: Path):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def out_text(contents: list[str], file_path: Path):

    with open(file_path, "wt", encoding="utf-8") as f:
        for line in contents:
            f.write(f"{line}\n")


def remove_files_and_dirs(lst_files_and_dirs: list[Path]):
    for file_or_dir in lst_files_and_dirs:
        if os.path.isfile(file_or_dir):
            os.remove(file_or_dir)
        elif os.path.isdir(file_or_dir):
            shutil.rmtree(file_or_dir)


def read_instances_from_csv(
    input_dir: Path, filename: str, create_method: Callable[..., T], primary_keys: list[str] = []
) -> list[T]:
    """パスをもとに csv ファイルを読み込み

    Args:
        input_dir (Path): 対象ファイルまでのパス
        filename (str): 対象ファイル名
        create_method (Callable[Any, T]): csv.DictReader が読み込んだ csv の行をパースした値を受け取り, クラスインスタンスを返す関数
        primary_keys (list[str]): 主キーとなる列名の一覧. もしあれば主キー制約に違反していないか確認する

    Returns:
        list[T]: `create_method` の出力インスタンスのリスト
    """
    results = []
    dict_pk_line_no: dict[tuple, int] = {}

    csv_file_path = input_dir.joinpath(filename)
    with open(csv_file_path) as csv_file:
        reader = DictReader(csv_file)
        for i, row in enumerate(reader):
            line_no = i + 2

            obj = create_method(**row)
            results.append(obj)

            # 主キー確認. もし主キーがなければ省略
            if len(primary_keys) == 0:
                continue
            pk = tuple(row[key] for key in primary_keys)
            if pk in dict_pk_line_no:
                raise ValueError(f"{dict_pk_line_no[pk]}行目と{line_no}行目がキー重複{pk}しています({filename})")

            dict_pk_line_no[pk] = line_no

    return results


def write_instances_to_csv(target_dir: Path, filename: str, instances: list[dict[str, Any]], header: list[str]):
    """パスをもとに csv ファイルを書き込み

    Args:
        target_dir (Path): 対象ファイルまでのパス
        filename (str): 対象ファイル名
        instances (list[dict]): 書き込み対象のインスタンス群を dict にパースしたもの
        header (list[str]): 列名の一覧
    """
    # ディレクトリがなければ作成
    create_dir_if_not_exists(target_dir)

    full_file_path = target_dir.joinpath(filename)
    with open(full_file_path, "wt", newline="") as f:
        writer = DictWriter(f, header)
        writer.writeheader()
        for instance in instances:
            writer.writerow(instance)
