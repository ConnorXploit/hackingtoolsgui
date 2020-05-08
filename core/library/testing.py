# import hackingtools as ht
# import unittest2 as unittest

# class MyTest(unittest.TestCase):

#     def test_ht_rsa_getRandomKeypair(self):
#         module = ht.getModule('rsa')
#         self.assertIsInstance(module.getRandomKeypair(3), tuple)

# if __name__ == "__main__":
#     unittest.main()

posibilidades = {
    "hex-lower": "0123456789abcdef",
    "hex-upper": "0123456789ABCDEF",
    "numeric": "0123456789",
    "numeric-space": "0123456789 ",
    "symbols14": "!@#$%^&*()-_+:",
    "symbols14-space": "!@#$%^&*()-_+: ",
    "symbols-all": "!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/",
    "symbols-all-space": "!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/ ",
    "ualpha": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ualpha-space": "ABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    "ualpha-symbol14": "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_+:",
    "ualpha-all": "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/",
    "ualpha-numeric": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "ualpha-numeric-space": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ",
    "ualpha-numeric-symbol14": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+:",
    "ualpha-numeric-symbol14-space": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+: ",
    "ualpha-numeric-all": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/",
    "ualpha-numeric-all-space": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/ ",
    "lalpha": "abcdefghijklmnopqrstuvwxyz",
    "lalpha-space": "abcdefghijklmnopqrstuvwxyz ",
    "lalpha-symbol14": "abcdefghijklmnopqrstuvwxyz!@#$%^&*()-_+:",
    "lalpha-all": "abcdefghijklmnopqrstuvwxyz!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/",
    "lalpha-numeric": "abcdefghijklmnopqrstuvwxyz0123456789",
    "lalpha-numeric-space": "abcdefghijklmnopqrstuvwxyz0123456789 ",
    "lalpha-numeric-symbol14": "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_+:",
    "lalpha-numeric-symbol14-space": "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_+: ",
    "lalpha-numeric-all": "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/",
    "lalpha-numeric-all-space": "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/ ",
    "mixalpha": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "mixalpha-space": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    "mixalpha-symbol14": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_+:",
    "mixalpha-all": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/",
    "mixalpha-numeric": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "mixalpha-numeric-space": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ",
    "mixalpha-numeric-symbol14": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+:",
    "mixalpha-numeric-symbol14-space": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+: ",
    "mixalpha-numeric-all": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/",
    "mixalpha-numeric-all-space": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+:~`[]{}|\\:;\"'<>,.?/ "
}

print(posibilidades.keys())

for pos in posibilidades:
    print(pos)

diccionario_seleccionado = None

while not diccionario_seleccionado:
    seleccion = input('Dime un diccionario a utilizar: ')
    if seleccion in posibilidades:
        diccionario_seleccionado = posibilidades[seleccion]
    else:
        print('{s} no existe'.format(s=seleccion))

longitud = None
while not longitud:
    longitud = int(input('Dime la longitud: '))
    if longitud <= 0:
        longitud = None

from itertools import product

for posib in product(diccionario_seleccionado, repeat=longitud):
    print(''.join(posib))
