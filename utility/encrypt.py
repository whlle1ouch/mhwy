import win32com.client as win32


def encrypt(key,content): # key:密钥,content:明文
    EncryptedData = win32.Dispatch('CAPICOM.EncryptedData')
    EncryptedData.Algorithm.KeyLength = 5
    EncryptedData.Algorithm.Name = 2
    EncryptedData.SetSecret(key)
    EncryptedData.Content = content
    return EncryptedData.Encrypt()



def decrypt(key,content): # key:密钥,content:密文
    EncryptedData = win32.client.Dispatch('CAPICOM.EncryptedData')
    EncryptedData.Algorithm.KeyLength = 5
    EncryptedData.Algorithm.Name = 2
    EncryptedData.SetSecret(key)
    EncryptedData.Decrypt(content)
    string = EncryptedData.Content
    return string