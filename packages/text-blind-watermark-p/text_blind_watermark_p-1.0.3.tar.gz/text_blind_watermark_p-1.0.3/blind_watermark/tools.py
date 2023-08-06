import numpy as np
import crypto
import sys

sys.modules['Crypto'] = crypto

from Crypto.Cipher import AES
import binascii


def one_dim_kmeans(inputs):
    e_tol = 10 ** (-6)

    center = [inputs.min(), inputs.max()]  # 1. 初始化中心点

    for i in range(300):
        threshold = (center[0] + center[1]) / 2
        is_class01 = inputs > threshold  # 2. 检查所有点与这k个点之间的距离，每个点归类到最近的中心
        center = [inputs[~is_class01].mean(), inputs[is_class01].mean()]  # 3. 重新找中心点
        if np.abs((center[0] + center[1]) / 2 - threshold) < e_tol:  # 4. 停止条件
            threshold = (center[0] + center[1]) / 2
            break

    is_class01 = inputs > threshold

    return is_class01


# %%



# %%
# 使bit类数据的0和1数量相同
def blance_bit():
    pass


def str_encrypt(text, password):
    text=text.encode('utf-8')
    cryptor = AES.new(key='{:0<16}'.format(password).encode('utf-8'),
                      mode=AES.MODE_ECB)  # key 长度必须是16,24,32 长度的 byte 格式

    ciphertext_tmp = cryptor.encrypt(text + b' ' * (16 - len(text) % 16))  # 明文的长度必须是16的整数倍
    ciphertext_tmp_hex = ciphertext_tmp.hex()  # 转16进制文本

    ciphertext_bin = bin(int(ciphertext_tmp_hex, 16))[2:]  # 转二进制

    ciphertext_arr = (np.array(list(ciphertext_bin)) == '1')

    return ciphertext_arr, len(ciphertext_arr)


def str_decrypt(ciphertext_arr, password):
    ciphertext_bin = ''.join(['1' if i else '0' for i in ciphertext_arr])
    ciphertext = hex(int(ciphertext_bin, base=2))[2:]
    text = AES.new(key='{:0<16}'.format(password).encode('utf-8'), mode=AES.MODE_ECB) \
        .decrypt(binascii.a2b_hex(ciphertext)).decode('utf-8')
    # 解密
    return text


if __name__ == "__main__":
    text = '加密文本。test!'
    password = '20190808'

    ciphertext_arr, len_ciphertext_arr = str_encrypt(text, password)

    text = str_decrypt(ciphertext_arr, password)

    print(text)


