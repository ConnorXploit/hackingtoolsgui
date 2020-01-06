import hackingtools as ht
import math
from getpass import getpass
import pkg_resources, inspect

HEADER_MENU = 'HackingTools v{v}'.format(v=pkg_resources.get_distribution('hackingtools').version)
MAX_ANCHOR_TITLE = len(HEADER_MENU) + 2

main_menu = ["Modules", "Categories", "Utils", "Pool", "Repositories", "APIs"]

api_dict = {}

def __createTable__(items, title='', force=None, back=False, exit_option=False):
    if items:
        used_title = HEADER_MENU if not title else title

        max_anchor_title = MAX_ANCHOR_TITLE if not title else len(title) + 2

        max_item_length = len(max(items, key=len)) + 4
        max_anchor_index = len(str(len(items)))
        max_anchor = max_item_length + 5 if max_item_length > max_anchor_title else max_anchor_title + 6

        max_anchor += int(len(str(len(items)).zfill(len(str(len(items))))))

        if max_anchor_title > max_anchor:
            max_anchor = max_anchor_title
        else:
            max_anchor_title = max_anchor

        print('|{a}|'.format(a='-'*(max_anchor+2)))

        print('| {h1}{t}{h2} |'.format(t=used_title, h1=' '*math.floor((max_anchor-len(used_title))/2), h2=' '*math.ceil((max_anchor-len(used_title))/2)))

        print('|{a}|'.format(a='-'*(max_anchor+2)))

        spaces = max_anchor - 5
        if type(items) == list:
            for index_t, t in enumerate(items):
                print('|  {n}) {m} {h} |'.format(n=str(index_t+1).zfill(max_anchor_index), m=t, h=' '*(spaces - len(t) - (len(str(index_t+1).zfill(max_anchor_index))-1))))
        else:
            for t in items:
                if items[t]:
                    print('{forced} {m}'.format(forced='-' if force and t in force else '*', m='{t} => {it}'.format(t=t, it=items[t])))
                else:
                    if t in api_dict:
                        items[t] = api_dict[t]
                        print('{forced} {m}'.format(forced='-' if force and t in force else '*', m='{t} => {it}'.format(t=t, it=api_dict[t])))
                    else:
                        print('{forced} {m}'.format(forced='-' if force and t in force else '*', m='{t} =>'.format(t=t)))
           
        if back:
            print('|  {h}|'.format(h=' '*(max_anchor)))
            print('|  {s}0) Back {h}|'.format(s=' '*(max_anchor_index-1), h=' '*(spaces-3+(max_anchor_index-3))))

        if exit_option:
            if not back:
                print('|  {h}|'.format(h=' '*(max_anchor)))
            print('| {s}-1) Exit {h}|'.format(s=' '*(max_anchor_index-1), h=' '*(spaces-3+(max_anchor_index-1))))

        print('|{a}|'.format(a='-'*(max_anchor+2)))

def menu(items, title='', force=None, back=False, exit_option=False):
    if items:
        __createTable__(items, title, force, back, exit_option)
        selected = -2
        min_option = 0 if not exit_option else -1
        while selected not in range(min_option, len(items)+1):
            try:
                if type(items) == list:
                    selected = int(input('  * Select an option: '))
                    if not selected in range(min_option, len(items)+1):
                        return menu(items, title, force, back, exit_option)
                else:
                    all_vars_setted = True
                    if force:
                        for f in force:
                            if f in items:
                                if items[f] == None:
                                    all_vars_setted = False

                    if all_vars_setted:
                        setted_value = input('  * You con now \'run\' for execute it (all params setted): ')
                    else:
                        setted_value = input('  * Set value (set VARIABLE value): ')
                    
                    if not setted_value == 'run':
                        try:
                            selected = int(setted_value.split(' ')[0])
                            if selected == 0:
                                return None
                        except:
                            selected = -2

                        var_setted = setted_value.split(' ')[1]
                        value_setted = ' '.join(setted_value.split(' ')[2:])
                        
                        if var_setted not in items:
                            print('Error on setted variable for this function')
                        else:
                            items[var_setted] = value_setted

                        return menu(items, title, force, back, exit_option)
                    else:
                        return items
            except:
                return menu(items, title, force, back, exit_option)
        
        if selected == 0:
            return None
        if selected == -1:
            return -1
        if type(items) == list:
            return items[selected-1]
        return items

    else:
        print('|--------------------------|')
        print('| No items to show in menu |')
        print('|--------------------------|')
        input('Press any key to continue back ')

def prepareFunctionParams(function_params):
    params = []
    if 'params' in function_params:
        params = function_params['params']
    
    default_params = {}
    if 'defaults' in function_params:
        default_params = function_params['defaults']

    full_params = {}

    for p in params:
        full_params[p] = None

    for p in default_params:
        full_params[p] = default_params[p]

    return (full_params, params)

def executeFunction(call_to_function, arguments):
    func_params = []
    for f in full_params:
        try:
            int(full_params[f])
            func_params.append('{var}={val}'.format(var=f, val=full_params[f]))
        except:
            func_params.append('{var}="{val}"'.format(var=f, val=full_params[f]))
    function_call_params = ','.join(func_params)
    res = None
    function_full_call = '{func}({pa})'.format(func=call_to_function, pa=function_call_params)
    res = eval(function_full_call)
    return res

if __name__ == "__main__":    
    value_selected = -2
    while not value_selected == -1:
        value_selected = menu(main_menu, exit_option=True)
        if value_selected == -1:
            print('|--------------------------|')
            print('|        Exiting :)        |')
            print('|--------------------------|')
        else:
            if value_selected == "Modules":

                module = menu(ht.getModulesNames(), 'Modules', back=True)

                if module:
                    functions_modules = menu(ht.getFunctionsNamesFromModule(module), 'Module {m}'.format(m=module), back=True)

                    function_params = ht.Utils.getFunctionsParams(category=ht.getModuleCategory(module), moduleName=module, functionName=functions_modules)

                    full_params, force_params = prepareFunctionParams(function_params)

                    full_params = menu(full_params, '{m} - {f}'.format(m=module, f=functions_modules), force=force_params, back=True)

                    if not full_params:
                        value_selected = -2
                    else:
                        call_to_function = 'ht.getModule("{mod}").{func}'.format(mod=module, func=functions_modules)
                        print(executeFunction(call_to_function, full_params))

                else:
                    value_selected = -2 # back

            elif value_selected == "Categories":

                category = menu(ht.getCategories(), 'Categories', back=True)

                if category:
                    module_in_category = menu(ht.getModulesFromCategory(category), 'Category {c}'.format(c=category), back=True)

                    if module_in_category:
                        functions_modules = menu(ht.getFunctionsNamesFromModule(module_in_category), 'Module {m}'.format(m=module_in_category), back=True)
                        print(functions_modules)

                    else:
                        value_selected = -2 # back

                else:
                    value_selected = -2 # back

            elif value_selected == "Utils":
                utils_options = ["IP Geolocation", "Random Text Generator", "Get Alphabet's Posibilities", "All Utils"]
                
                option_utils = menu(utils_options, 'Utils', back=True)

                if option_utils == "IP Geolocation":
                    ip_setted = input('Set IP: ')
                    print(ht.Utils.getIPLocationGPS_v2(ip_setted))

                elif option_utils == "Random Text Generator":
                    length_setted = input('Set length (default: 8): ')

                    alphabet_setted = input('Set alphabet (default: lalpha): ')

                    if not length_setted:
                        length_setted = 8

                    if not alphabet_setted:
                        alphabet_setted = 'lalpha'

                    print(ht.Utils.randomText(length=length_setted, alphabet=alphabet_setted))

                elif option_utils == "Get Alphabet's Posibilities":
                    print('\n'.join(ht.Utils.getPosibleAlphabet()))
                
                elif option_utils == "All Utils":
                    utils_all_functions = [ i.split('(')[0] for i in inspect.getsource(ht.Utils).split('def ') ]
                    utils_selected_func = menu(utils_all_functions, 'Utils Functions', back=True)

                    utils_func_parameters = ht.Utils.getAnyFunctionParams('ht.Utils.{utils_func}'.format(utils_func=utils_selected_func))

                    full_params, force_params = prepareFunctionParams(utils_func_parameters)

                    full_params = menu(full_params, 'Utils {fun}'.format(fun=utils_selected_func), force=force_params, back=True)

                    if not full_params:
                        value_selected = -2
                    else:
                        call_to_function = 'ht.Utils.{func}'.format(func=utils_selected_func)
                        print(executeFunction(call_to_function, full_params))
                
            elif value_selected == "Pool":

                pool_node = menu(sorted(ht.Pool.getPoolNodes()), 'Pool Nodes', back=True)
                print(pool_node)

            elif value_selected == "Repositories":

                repo_server = menu(ht.Repositories.getOnlineServers(), 'Repositories', back=True)
                print(repo_server)

            elif value_selected == "APIs":
                apis_option_menu = ["Add Manually", "Load file .htpass"]

                option_apis = menu(apis_option_menu, 'Set APIs', back=True)

                if option_apis == "Add Manually":
                    for api_key in ht.Config.getAPIsNames():
                        api_dict[api_key] = ht.Config.getAPIKey(api_key)
                    menu(api_dict, 'APIs', back=True)

                elif option_apis == "Load file .htpass":
                    file_path = input('Set the path to the .htpass file: ')
                    file_pass = getpass('Password File: ')

                    ht.Config.loadRestAPIsFile(file_path, file_pass)

                    for api_key in ht.Config.getAPIsNames():
                        api_dict[api_key] = ht.Config.getAPIKey(api_key)
                    menu(api_dict, 'APIs', back=True)
