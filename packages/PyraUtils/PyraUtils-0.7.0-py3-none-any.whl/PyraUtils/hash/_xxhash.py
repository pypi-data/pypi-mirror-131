# -*- coding: utf-8 -*-

"""
created by：2017-05-10 20:11:31
modify by: 2017-06-13 09:38:36

功能：实现xxhash模块的二次封装；
    实现对文件，对字节流的xxhash32或者xxhash64的加密。
    根据需求可以返回intdigest, digest, hexdigest中的一种。

参考文档：
    https://github.com/ifduyue/python-xxhash
"""

import xxhash

class XxHashUtil:
    """计算文件或字节流的xxhash值, 工具类"""

    @staticmethod
    def get_xxhash_of_data(bytes_data, xxhash_type=64, digest="digest", seednum=0):
        """计算字节流的xxHash值

        参数:

            bytes_data: 字节流；bytes。
            xxhash_type: xxhash32 or xxhash64，默认值为64，即xxhash64; int。
            digest: 返回值类型,可选值: intdigest, digest, hexdigest；默认为digest; string。
            seednum： seed 值，默认值为0；int。

        返回:

        返回类型:
            int or string
        """

        if xxhash_type == 32:
            h = xxhash.xxh32(seed=seednum)
        elif xxhash_type == 64:
            h = xxhash.xxh64(seed=seednum)
        else:
            raise ValueError("xxhash-Type is error!")

        if bytes_data is not None:
            h.update(bytes_data)
        else:
            raise RuntimeError("The data not allow None")

        if digest == "intdigest":
            return h.intdigest()
        elif digest == "hexdigest":
            return h.hexdigest()
        elif digest == "digest":
            return h.digest()
        else:
            raise ValueError("digest is error!")

