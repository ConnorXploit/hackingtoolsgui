from datetime import datetime
import os as __os
from . import Config, Logger, Utils, UtilsDjangoViewsAuto
if Utils.amIdjango(__name__):
    from core.library import hackingtools as ht
else:
    import hackingtools as ht
ht.Logger.setDebugModule(True)


__config_locales__ = ht.Config.getConfig(parentKey='core', key='locales')


def __createModuleFunctionView__(category, moduleName, functionName, is_main=False):
    try:
        # Creates the JSON config for the view modal form
        functionParams = Utils.getFunctionsParams(
            category=category, moduleName=moduleName, functionName=functionName)

        # Get posible functions with args that uses values from another func
        funcsFromFunc = None if not hasattr(ht.getModule(
            moduleName), '_funcArgFromFunc_') else dict(ht.getModule(moduleName)._funcArgFromFunc_)

        moduleViewConfig = {}

        moduleViewConfig['__function__'] = functionName

        if not is_main:
            moduleViewConfig['__async__'] = False

            if ht.Utils.doesFunctionContainsExplicitReturn(ht.Utils.getFunctionFullCall(moduleName, ht.getModuleCategory(moduleName), functionName)):
                moduleViewConfig['__return__'] = 'text'
            else:
                moduleViewConfig['__return__'] = ''

        if not functionParams:
            # Retry for reload
            functionParams = ht.Utils.getFunctionsParams(
                category=category, moduleName=moduleName, functionName=functionName)

        if functionParams:
            if 'params' in functionParams:
                for param in functionParams['params']:
                    moduleViewConfig[param] = {}
                    moduleViewConfig[param]['__type__'] = 'file' if 'file' in str(
                        param).lower() else ht.Utils.getValueType(str(param))
                    moduleViewConfig[param]['label_desc'] = param
                    moduleViewConfig[param]['placeholder'] = param
                    moduleViewConfig[param]['required'] = True

            if 'defaults' in functionParams:
                for param in functionParams['defaults']:
                    moduleViewConfig[param] = {}
                    moduleViewConfig[param]['__type__'] = 'file' if 'file' in str(param).lower(
                    ) else ht.Utils.getValueType(str(functionParams['defaults'][param]))
                    moduleViewConfig[param]['label_desc'] = param
                    moduleViewConfig[param]['placeholder'] = param
                    moduleViewConfig[param]['value'] = functionParams['defaults'][param]
                    if moduleViewConfig[param]['__type__'] == 'checkbox':
                        moduleViewConfig[param]['selected'] = moduleViewConfig[param]['value']

            # Create the data for auto fill the param with another funcs return
            if funcsFromFunc and functionName in funcsFromFunc and len(funcsFromFunc[functionName]) > 0:
                for arg in funcsFromFunc[functionName]:
                    if arg in moduleViewConfig:
                        if not 'options_from_function' in moduleViewConfig[arg]:
                            moduleViewConfig[arg]['options_from_function'] = {}
                        for moduleToExecute in funcsFromFunc[functionName][arg]:
                            moduleViewConfig[arg]['options_from_function'][moduleToExecute] = funcsFromFunc[functionName][arg][moduleToExecute]
        else:
            ht.Logger.printMessage(
                message='No function params', description=functionName, debug_core=True)

        # Add pool it checkbox
        pool_param = '__pool_it_{p}__'.format(p=functionName)
        moduleViewConfig[pool_param] = {}
        moduleViewConfig[pool_param]['__type__'] = 'checkbox'
        moduleViewConfig[pool_param]['label_desc'] = 'Pool the execution to the pool list'
        moduleViewConfig[pool_param]['selected'] = False

        if is_main:
            moduleViewConfig['close'] = {}
            moduleViewConfig['close']['__type__'] = 'button'
            moduleViewConfig['close']['value'] = 'Close'

            moduleViewConfig['submit'] = {}
            moduleViewConfig['submit']['__id__'] = functionName
            moduleViewConfig['submit']['__type__'] = 'submit'
            if functionName:
                moduleViewConfig['submit']['value'] = ' '.join(
                    [x.capitalize() for x in functionName.split('_')])
            moduleViewConfig['submit']['loading_text'] = '{m}ing'.format(
                m=moduleName.replace('ht_', ''))

        Config.__save_django_module_config__(
            moduleViewConfig, category, moduleName, functionName, is_main=is_main)
        Config.switch_function_for_map(category, moduleName, functionName)
        ht.Config.__look_for_changes__()
        ht.Logger.printMessage(
            message='Creating Function Modal View', description=functionName, debug_core=True)
        return {functionName: moduleViewConfig}
    except Exception as e:
        Logger.printMessage(str(e), is_error=True)
        return None


def __getModulesGuiNames__():
    """Return's an Array with the Label for GUI for that module

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    names = {}
    for tool in ht.getModulesNames():
        label = ht.Config.getConfig(
            parentKey='modules', key=tool, subkey='__gui_label__')
        if label:
            names[tool] = label
    return names


def __getModulesModalTests__():
    """Return's an Array with all modules as keys and their values, the Modal GUI function forms

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    tools_functions = {}
    for tool in ht.getModulesNames():
        tool_functions = Config.getConfig(
            parentKey='modules', key=tool, subkey='django_form_module_function')
        if tool_functions:
            tools_functions[tool] = tool_functions
    return tools_functions


def __getModulesFunctionsCalls__():
    """Return's an Array with modules name as keys and inside it's values, 
    the key are the functions call names with a value of a template for 
    initialaizing and calling that function

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    modulesCalls = {}
    header = "# Get the module from hackingtools\nht_loaded_{module_name} = ht.getModule(\"{module_name}\"){header_params}\n\n# Call the module\'s function for getting a result\nmod_result = ht_loaded_{module_name}.{module_function}({params})\n\n# Return it\nprint(mod_result)"

    header_params = {}
    header_params_arg = {}
    for module in ht.__modules_loaded__:
        if not module in header_params:
            header_params[module] = {}
        if not module in header_params_arg:
            header_params_arg[module] = {}
        for func in ht.__modules_loaded__[module]:
            if not func in header_params[module]:
                header_params[module][func] = "\n\n# Load the params you need\nparams = {}"
            if not func in header_params_arg[module]:
                header_params_arg[module][func] = []
            try:
                if 'original_params' in ht.__modules_loaded__[module][func]:
                    required_params = None
                    default_params = None
                    for param in ht.__modules_loaded__[module][func]['original_params']:

                        if 'params' == param:
                            required_params = ht.__modules_loaded__[
                                module][func]['original_params'][param]
                            for reqpar in required_params:
                                header_params[module][func] += '\n\nparams[\'{p}\'] = input(\'Set the param {p}: \')'.format(
                                    p=reqpar)
                                header_params_arg[module][func].append(
                                    '{p}=params[\'{p}\']'.format(p=reqpar))

                        if 'defaults' == param:
                            default_params = ht.__modules_loaded__[
                                module][func]['original_params'][param]
                            for defpar in default_params:
                                if default_params[defpar] == 'None' or default_params[defpar] == None or isinstance(default_params[defpar], int) or isinstance(default_params[defpar], list) or isinstance(default_params[defpar], dict):
                                    header_params[module][func] += '\n\nparams[\'{p}\'] = input(\'Set the param {p} (Default value: {d}): \')\nif not params[\'{p}\']:\n\tparams[\'{p}\'] = {d}'.format(
                                        p=defpar, d=default_params[defpar])
                                else:
                                    header_params[module][func] += '\n\nparams[\'{p}\'] = input(\'Set the param {p} (Default value: {d}): \')\nif not params[\'{p}\']:\n\tparams[\'{p}\'] = \'{d}\''.format(
                                        p=defpar, d=default_params[defpar])
                                header_params_arg[module][func].append(
                                    '{p}=params[\'{p}\']'.format(p=defpar))

            except:
                header_params[module][func] = ''
    for module in ht.__modules_loaded__:
        module_funcs = {}
        for func in ht.__modules_loaded__[module]:
            try:
                for param in ht.__modules_loaded__[module][func]['original_params']:
                    moduleParams = ht.__modules_loaded__[
                        module][func]['original_params'][param]
                    if not moduleParams:
                        moduleParams = []
                    module_funcs[func] = header.format(header_params=header_params[module][func], module_name=module.split(
                        '.')[-1], module_function=func, module_function_params=', '.join(moduleParams), params=', '.join(header_params_arg[module][func]))
            except:
                try:
                    module_funcs[func] = header.format(header_params=header_params[module][func], module_name=module.split('.')[-1], module_function=func, module_function_params='')
                except:
                    pass
        modulesCalls[module.split('.')[-1]] = module_funcs
    return modulesCalls


def __getModulesFunctionsForMap__():
    functions = {}
    for module in ht.__modules_loaded__:
        functions[module.split('.')[-1]] = []
        for f in ht.__modules_loaded__[module]:
            functionName = f.split('.')[-1]
            conf_func = Config.getConfig(parentKey='django', key='maps', subkey=module.split(
                '.')[-1], extrasubkey=functionName)

            if not conf_func:
                Config.switch_function_for_map(ht.getModuleCategory(
                    module.split('.')[-1]), module.split('.')[-1], functionName)
            else:
                in_maps = '__in_map_{f}__'.format(f=functionName)

                if in_maps in conf_func and conf_func[in_maps] == True:
                    functions[module.split('.')[-1]].append(functionName)

        if not functions[module.split('.')[-1]]:
            functions[module.split('.')[-1]] = []

    return functions


def __getModulesConfig_treeView__():
    """Return a String with the config for the GUI Treeview

    Parameters
    ----------
        None

    Return
    ----------
        String
    """
    result_text = []
    tools_config = ht.__getModulesFullConfig__()
    __treeview_load_all__(config=tools_config, result_text=result_text)
    response = ','.join(result_text)
    return response


def __regenerateConfigView__(moduleName):
    Config.__regenerateConfigModulesDjango__(
        {}, ht.getModuleCategory(moduleName), moduleName)


def __getReturnAsModalHTML__(response, main=True):
    res = ''
    default_classnames_per_type = Config.getConfig(
        parentKey='django', key='html', subkey='modal_forms', extrasubkey='default_types')
    res_type = Utils.getValueType(response, getResponse=True)
    if isinstance(response, dict):
        for key, val in response.items():
            if val is not None:
                val_type_temp = Utils.getValueType(
                    val, getResponse=True, returnLiteralType=True)
                if val_type_temp == list:
                    res += "<label for=\"{id}\">{input_label_desc}</label>".format(
                        id=key, input_label_desc=key)
                    res += __getReturnAsModalHTML__(list(val), main=False)
                # elif val_type_temp == dict:
                #     res += __getReturnAsModalHTML__(val, main=False)
                else:
                    val_type = Utils.getValueType(val, getResponse=True)
                    try:
                        input_className = default_classnames_per_type[val_type]['__className__']
                    except:
                        input_className = ''

                    if val_type == 'checkbox':
                        if not val:
                            res += "</br><div class=\"toggle btn waves-effect waves-light btn-warning off\" data-toggle=\"toggle\" style=\"width: 0px; height: 0px;\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"primary\" data-offstyle=\"warning\" id=\"{id}\" name=\"{id}\" disabled><div class=\"toggle-group\"><label class=\"btn btn-primary toggle-on waves-effect waves-light\">On</label><label class=\"btn btn-warning active toggle-off waves-effect waves-light\">Off</label><span class=\"toggle-handle btn btn-default waves-effect waves-light\"></span></div></div><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></br></br>".format(
                                id=key, input_label_desc=key)
                        else:
                            res += "</br><div class=\"toggle btn waves-effect waves-light btn-primary\" data-toggle=\"toggle\" style=\"width: 0px; height: 0px;\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"primary\" data-offstyle=\"warning\" id=\"{id}\" name=\"{id}\" disabled><div class=\"toggle-group\"><label class=\"btn btn-primary toggle-on waves-effect waves-light\">On</label><label class=\"btn btn-warning active toggle-off waves-effect waves-light\">Off</label><span class=\"toggle-handle btn btn-default waves-effect waves-light\"></span></div></div><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></br></br>".format(
                                id=key, input_label_desc=key)

                    elif val_type == 'number':
                        res += "<div class='md-form'><label for=\"{id}\">{input_label_desc}</label><input class=\"{className}\" type=\"number\" value=\"{input_value}\" name=\"{id}\" /></div>".format(
                            id=key, input_label_desc=key, className=input_className, input_value=val)

                    elif val_type == 'textarea':
                        res += "<div class=\"md-form\"><label for=\"{id}\">{input_label_desc}</label><textarea class=\"{className}\" name=\"{id}\" id=\"{id}\" rows=\"{rows}\">{value}</textarea></div>".format(
                            className=input_className, id=key, input_label_desc=key, value=val, rows=int(int(len(val)/80) + val.count('\n')))

                    elif val_type == 'image':
                        res += "<div class='md-form'><label for=\"{id}\">{input_label_desc}</label></br><img src=\"{input_value}\" name=\"{id}\" class=\"response_image\" /></div>".format(
                            id=key, input_label_desc=key, className=input_className, input_value=val)

                    elif val_type == 'time':
                        val = val.strftime("%d-%m-%Y %H:%M:%S")
                        res += "<div class='md-form'><label for=\"{id}\">{input_label_desc}</label><input class=\"{className}\" type=\"text\" value=\"{input_value}\" name=\"{id}\" /></div>".format(
                            id=key, input_label_desc=key, className=input_className, input_value=val)
                    else:
                        res += "<div class='md-form' id=\"{id}\"><label for=\"{id}\">{input_label_desc}</label>".format(
                            id=key, input_label_desc=key)
                        res += __getReturnAsModalHTML__(val, main=False)
                        res += "</div>"
    elif isinstance(response, bool):
        return "<div class=\"checkbox\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"primary\" data-offstyle=\"warning\" {checked} disabled></div><br />".format(checked=response)
    elif isinstance(response, int):
        val_type = Utils.getValueType(response, getResponse=True)
        try:
            input_className = default_classnames_per_type[val_type]['__className__']
        except:
            input_className = ''
        return "<div class='md-form'><input class=\"{className}\" type=\"number\" value=\"{input_value}\" /></div>".format(className=input_className, input_value=response)
    elif res_type == 'select':
        if isinstance(response, str):
            response = list(response)

        use_hr = False
        for r in response:
            res += "<ul class=\"list-group list-group-flush\">"

            if isinstance(r, str) and Utils.getValueType(r, getResponse=True) == 'text':
                try:
                    input_className = default_classnames_per_type['text']['__className__']
                except:
                    input_className = ''

                form = 'md-form'
                if not main:
                    form = 'md-form-item'
                res += "<div class='{form}'><input class=\"{className}\" type=\"text\" value=\"{input_value}\" name=\"{id}\" /></div>".format(
                    form=form, id=r, className=input_className, input_value=r)
            else:
                use_hr = True
                res += "<li class=\"list-group-item\">{value}</li>".format(
                    value=__getReturnAsModalHTML__(r, False))

            res += "</ul>"

            if not main and len(response) > 1 and use_hr:
                res += "<hr class='sidebar-divider my-0 my-separator-response'>"
    else:
        val_type = Utils.getValueType(response, getResponse=True)
        try:
            input_className = default_classnames_per_type[val_type]['__className__']
        except:
            input_className = ''
        if val_type == 'checkbox':
            if not response:
                return "</br><div class=\"toggle btn waves-effect waves-light btn-warning off\" data-toggle=\"toggle\" style=\"width: 0px; height: 0px;\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"primary\" data-offstyle=\"warning\" id=\"{id}\" name=\"{id}\" disabled><div class=\"toggle-group\"><label class=\"btn btn-primary toggle-on waves-effect waves-light\">On</label><label class=\"btn btn-warning active toggle-off waves-effect waves-light\">Off</label><span class=\"toggle-handle btn btn-default waves-effect waves-light\"></span></div></div><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></br></br>".format(id=response, input_label_desc=response)
            return "</br><div class=\"toggle btn waves-effect waves-light btn-primary\" data-toggle=\"toggle\" style=\"width: 0px; height: 0px;\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"primary\" data-offstyle=\"warning\" id=\"{id}\" name=\"{id}\" disabled><div class=\"toggle-group\"><label class=\"btn btn-primary toggle-on waves-effect waves-light\">On</label><label class=\"btn btn-warning active toggle-off waves-effect waves-light\">Off</label><span class=\"toggle-handle btn btn-default waves-effect waves-light\"></span></div></div><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></br></br>".format(id=response, input_label_desc=response)
        elif val_type == 'data' or val_type == 'textarea':
            return "<div class=\"md-form\"><label for=\"response-{id}\">data</label><textarea class=\"{className}\" name=\"response-{id}\" id=\"response-{id}\" rows=\"{rows}\">{value}</textarea></div>".format(className=input_className, id=response[0], value=response, rows=int(int(len(response)/80) + response.count('\n')))
        elif val_type == 'password':
            return "<div class='md-form'><input class=\"{className}\" type=\"password\" value=\"{input_value}\"/></div>".format(className=input_className, input_value=response)
        elif val_type == 'image':
            return "<div class='md-form'><label for=\"response-img\">image</label></br><img src=\"{input_value}\" name=\"response-img\" class=\"response_image\" /></div>".format(className=input_className, input_value=response)
        else:
            # if val_type == 'url':
            #     return "<button class=\"btn\" data-clipboard-target=\"#response\"><img src=\"/static/core/img/clippy.svg\" alt=\"Copy to clipboard\"></button><div class='md-form'><input class=\"{className}\" type=\"text\" id=\"response\" value=\"{input_value}\"/></div>".format(className=input_className, input_value=response)
            return "<div class='md-form'><input class=\"{className}\" type=\"text\" id=\"response\" value=\"{input_value}\"/></div>".format(className=input_className, input_value=response)
    return res


# TreeView for Modules Configuration in Modal Panel
global __treeview_counter__
__treeview_counter__ = 0

# ! Slows down the first load of HT in Django or the calls to "home"


def __treeview_load_all__(config, result_text, count=0, count_pid=-1):
    """Loads the GUI Treeview with the config of all the modules loaded

    Parameters
    ----------
        config = Array
        result_text = String
        count = int
        count_pid = int

    Return
    ----------
        None
    """
    count += 1
    count_pid += 1
    for c in config:
        count += 1
        count = __treeview_count__(count)
        result_text.append(__treeview_createJSON__(
            conf_key=config[c], key=c, count=count, pid=count_pid))
        ht.Logger.printMessage('{msg} - {key} - {n} - {m}'.format(
            msg='Pasando por: ', key=c, n=count, m=count_pid), is_warn=True, debug_core=True)
        if not isinstance(config[c], str) and not isinstance(config[c], bool) and not isinstance(config[c], int) and not isinstance(config[c], float):
            try:
                __treeview_load_all__(
                    config=config[c], result_text=result_text, count=count, count_pid=count-1)
                count += 1
            except:
                try:
                    __treeview_load_all__(config=tuple(
                        config[c]), result_text=result_text, count=count, count_pid=count-1)
                    count += 1
                    ht.Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=__config_locales__[
                                           'error_json_data_loaded'], key=c, conf_key=config[c]), is_warn=True, debug_core=True)
                except:
                    ht.Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=__config_locales__[
                                           'error_json_data_not_loaded'], key=c, conf_key=config[c]), color=ht.Logger.__Fore.RED, debug_core=True)
        count += 1


def __treeview_count__(count):
    global __treeview_counter__
    if count < __treeview_counter__:
        count = __treeview_counter__
    count += 1
    __treeview_counter__ = count
    return count


def __treeview_createJSON__(conf_key, key, count=1, pid=0):
    """Return JSON String with the config for the treeview

    Parameters
    ----------
        conf_key = String
        key = String
        count = int
        pid = int

    Return
    ----------
        String JSON Format
    """
    try:
        open_key = "{"
        close_key = "}"
        if isinstance(conf_key, str):
            return '{open_key}id:{count},name:"{name}",pid:{pid},value:"{value}"{close_key}'.format(open_key=open_key, count=count, name=key, pid=pid, value=conf_key, close_key=close_key)
        else:
            return '{open_key}id:{count},name:"{name}",pid:{pid},value:""{close_key}'.format(open_key=open_key, count=count, name=key, pid=pid, close_key=close_key)
    except:
        ht.Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=__config_locales__[
                               'error_load_json_data'], key=key, conf_key=conf_key), is_error=True)

# End of TreeView

# Core


def __getModulesDjangoForms__():
    forms = {}
    for mod in ht.getModulesNames():
        form = __createHtmlModalForm__(mod)
        if form:
            for url in form:
                if form[url]:
                    forms[mod] = form
    return forms


def __createHtmlModalForm__(mod, config_subkey='django_form_main_function', config_extrasubkey=None, session_id=None):
    module_form = Config.getConfig(
        parentKey='modules', key=mod, subkey=config_subkey, extrasubkey=config_extrasubkey)
    functionModal = Config.getConfig(
        parentKey='modules', key=mod, subkey=config_subkey, extrasubkey='__function__')
    default_classnames_per_type = Config.getConfig(
        parentKey='django', key='html', subkey='modal_forms', extrasubkey='default_types')

    if not module_form:
        return

    html = "<div class=\"modal-body\">"
    footer = '<div class="modal-footer">'
    m_form = module_form

    # For ajax
    submit_id = ''

    if '__function__' in m_form:
        submit_id = 'submit_{mod}_{name}'.format(
            mod=mod, name=m_form['__function__'])

    for m in m_form:
        temp_m_form = m_form
        if not m == '__async__' and not m == '__function__' and not '__separator' in m and (isinstance(temp_m_form, dict) and (('systems' in temp_m_form[m] and __os.name in temp_m_form[m]['systems']) or not 'systems' in temp_m_form[m])):
            if '__type__' in temp_m_form[m]:
                input_type = temp_m_form[m]['__type__']

                input_className = ''
                if not input_type in default_classnames_per_type:
                    ht.Logger.printMessage(message='__createHtmlModalForm__', description='There is no __className__ defined for this type of input \'{input_type}\''.format(
                        input_type=input_type), color=ht.Logger.__Fore.YELLOW)
                else:
                    input_className = default_classnames_per_type[input_type]['__className__']

                input_placeholder = ''
                if 'placeholder' in temp_m_form[m]:
                    input_placeholder = temp_m_form[m]['placeholder']

                input_label_desc = ''
                if 'label_desc' in temp_m_form[m]:
                    input_label_desc = temp_m_form[m]['label_desc']

                input_value = ''
                if 'value' in temp_m_form[m]:
                    input_value = temp_m_form[m]['value']

                if 'api' in m:
                    input_value = Config.getAPIKey('{m}_api'.format(
                        m=mod.split('_')[-1]), session_id=session_id)
                    input_className = ' '.join([input_className, 'apiKey'])

                if input_value != 0 and (not input_value or 'None' == input_value or 'null' == input_value):
                    input_value = ''

                checkbox_selected = False
                if 'selected' in temp_m_form[m]:
                    checkbox_selected = temp_m_form[m]['selected']

                loading_text = ''
                if 'loading_text' in temp_m_form[m]:
                    loading_text = temp_m_form[m]['loading_text']

                required = ''
                if 'required' in temp_m_form[m] and temp_m_form[m]['required'] == True:
                    required = 'required'

                # Creates a select if any options are filled by another func
                # try:
                #     options_from_function = []
                #     if 'options_from_function' in temp_m_form[m]:
                #         options_from_function = temp_m_form[m]['options_from_function']
                #         for optModuleName in options_from_function:
                #             if optModuleName in ht.getModulesNames() or optModuleName in [moduleNm.replace('ht_', '') for moduleNm in ht.getModulesNames()]:
                #                 functionCall = 'ht.getModule(\'{mod}\').{func}()'.format(
                #                     mod=optModuleName, func=temp_m_form[m]['options_from_function'][optModuleName])
                #                 options_from_function = eval(functionCall)
                #             elif 'core' == optModuleName:
                #                 functionCall = 'ht.{func}()'.format(
                #                     func=temp_m_form[m]['options_from_function'][optModuleName])
                #                 options_from_function = eval(functionCall)
                #             else:
                #                 functionCall = '{m}.{func}()'.format(
                #                     m=optModuleName, func=temp_m_form[m]['options_from_function'][optModuleName])
                #                 options_from_function = eval(functionCall)
                # except Exception as e:
                #     Logger.printMessage(str(e), is_error=True)
                try:
                    options_from_function = []
                    if 'options_from_function' in temp_m_form[m]:
                        options = temp_m_form[m]['options_from_function']
                        for optModuleName in options:
                            if optModuleName in ht.getModulesNames() or optModuleName in [moduleNm.replace('ht_', '') for moduleNm in ht.getModulesNames()]:
                                functionCall = 'ht.getModule(\'{mod}\').{func}()'.format(
                                    mod=optModuleName, func=temp_m_form[m]['options_from_function'][optModuleName])
                                options_from_function = [functionCall]
                            elif 'core' == optModuleName:
                                functionCall = 'ht.{func}()'.format(
                                    func=temp_m_form[m]['options_from_function'][optModuleName])
                                options_from_function = [functionCall]
                            else:
                                functionCall = '{m}.{func}()'.format(
                                    m=optModuleName, func=temp_m_form[m]['options_from_function'][optModuleName])
                                options_from_function = [functionCall]
                except Exception as e:
                    Logger.printMessage(str(e), is_error=True)
                    options_from_function = []

                if options_from_function:
                    input_type = 'select'

                if input_type == 'file':
                    html += "<div class='input-group'>"
                    html += "<input type='file' class='custom-file-input' name='{id}' {required}>".format(
                        id=m, required=required)
                    html += "<label class='custom-file-label' for='{id}'>Choose file</label>".format(
                        id=m)
                    html += "</div>"

                elif input_type == 'checkbox':
                    checkbox_disabled = ''
                    color_on = 'primary'
                    color_off = 'warning'

                    if '__pool_it_' in m and not ht.__WANT_TO_BE_IN_POOL__:
                        checkbox_disabled = 'disabled'
                        color_on = 'default'
                        color_off = 'default'

                    if checkbox_selected:
                        html += "<div class=\"checkbox\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"{color_on}\" data-offstyle=\"{color_off}\" id=\"{id}\" name=\"{id}\" {required} checked {disabled}><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></div><br />".format(
                            color_on=color_on, color_off=color_off, id=m, input_label_desc=input_label_desc, required=required, disabled=checkbox_disabled)
                    else:
                        html += "<div class=\"checkbox\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"{color_on}\" data-offstyle=\"{color_off}\" id=\"{id}\" name=\"{id}\" {required} {disabled}><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></div><br />".format(
                            color_on=color_on, color_off=color_off, id=m, input_label_desc=input_label_desc, required=required, disabled=checkbox_disabled)

                elif input_type == 'select':

                    html += "<span class=\"name-select\" value=\"{placeholder}\">{placeholder}</span><select id=\"editable-select-{mod}-{id}-{config_subkey}\" name=\"{id}\" placeholder=\"{placeholder}\" class=\"{className}\" {required}>".format(
                        placeholder=input_placeholder, className=input_className, mod=mod, id=m, required=required, config_subkey=config_subkey)
                    html += "<option value='{input_value}' selected>{input_value}</option>".format(input_value=input_value)

                    # if input_value in options_from_function:
                    #     options_from_function.remove(input_value)

                    # for func in options_from_function:
                    #     html += "<option value='{cat}'>{cat}</option>".format(
                    #         cat=func)

                    html += "</select><script>$('#editable-select-{mod}-{id}-{config_subkey}').editableSelect();".format(mod=mod, id=m, config_subkey=config_subkey)

                    if required != '':
                        html += "$('#editable-select-{mod}-{id}-{config_subkey}').prop('required',true);".format(mod=mod, id=m, config_subkey=config_subkey)

                    options = temp_m_form[m]['options_from_function']
                    for optModuleName in options:
                        datos = {}
                        datos['mod'] = optModuleName
                        datos['argument'] = m
                        datos['typeFunction'] = config_subkey
                        if config_extrasubkey:
                            datos['origFunction'] = config_extrasubkey

                        html += "$( document ).ready(function(){"
                        html += "$.ajax({"
                        html += "cache: false, processData: false, dataType: 'json', contentType: 'application/json', "
                        html += "url: '/core/loadcontentfunctionparam/', type : 'POST', async: true, "
                        html += "data: JSON.stringify({datos}),".format(datos=datos)
                        html += "success: function(data){"
                        html += "var array = data.data;"
                        html += "if (array != '')"
                        html += "{"
                        html += "for (i in array) {"                    
                        html += "$(\"#editable-select-{mod}-{id}-{config_subkey}\").next().next().append('<li value=\"'+array[i]+'\" class=\"es-visible\">'+array[i]+'</li>');".format(mod=mod, id=m, config_subkey=config_subkey)
                        html += "}"
                        html += "}"
                        html += "},"
                        html += "error: function (xhr, ajaxOptions, thrownError) {"
                        html += "var errorMsg = 'Ajax request failed: ' + xhr.responseText;"
                        html += "console.log(errorMsg);"
                        html += "}"
                        html += "});"
                        html += "});"

                    html += "</script>"

                elif input_type == 'button':

                    footer += "<button type=\"button\" class=\"{className}\" data-dismiss=\"modal\">{input_value}</button>".format(
                        className=input_className, input_value=input_value)

                elif input_type == 'submit':

                    submit_id = '{m}_{f}'.format(m=m, f=config_extrasubkey)
                    if config_subkey == 'django_form_main_function':
                        footer += "<input type=\"submit\" class=\"{className}\" value=\"Run\" id=\"submit_main_{id}\" />".format(
                            className=input_className, id=mod)
                    else:
                        footer += "<input type=\"submit\" class=\"{className}\" value=\"{input_value}\" id=\"{id}\" />".format(
                            className=input_className, input_value=input_value, id=submit_id)

                    if loading_text:
                        footer += "<script>$('#"
                        footer += m
                        footer += "').on('click', function(e){$('#"
                        footer += m
                        footer += "').attr('value', '{loading_text}'); e.preventDevault();".format(
                            loading_text=loading_text)
                        footer += "});</script>"

                elif input_type == 'textarea':

                    if input_label_desc:
                        html += "<div class=\"form-group row\"><label for=\"{id}\" class=\"col-4 col-form-label label-description\">{input_label_desc}</label><div class=\"col-4\"><textarea class=\"{className}\" name=\"{id}\" id=\"{id}\" rows=\"{rows}\" placeholder=\"{placeholder}\"></textarea></div></div>".format(
                            className=input_className, id=m, placeholder=input_placeholder, input_label_desc=input_label_desc, rows=str(int(len(input_placeholder)/100) + input_placeholder.count('\n')))
                    else:
                        html += "<textarea class=\"{className}\" name=\"{id}\" id=\"{id}\" rows=\"{rows}\" placeholder=\"{placeholder}\"></textarea>".format(
                            className=input_className, id=m, placeholder=input_placeholder, rows=str(int(len(input_placeholder)/100) + input_placeholder.count('\n')))

                else:
                    html += "<div class='md-form'><label for=\"{id}\">{input_label_desc}</label><input class=\"{className}\" type=\"{input_type}\" value=\"{input_value}\" placeholder=\"{placeholder}\" name=\"{id}\" {required}/></div>".format(
                        id=m, placeholder=input_placeholder, input_label_desc=input_label_desc, className=input_className, input_type=input_type, input_value=input_value, required=required)

        if '__separator' in m and '__' == m[-2:] and m_form[m] == True:
            html += "<hr class='sidebar-divider my-0 my-separator'>"

    for m in m_form:
        if '__async__' == m and m_form[m]:
            html += "<input type='text' value='true' id='is_async' hidden />"

    if config_subkey == 'django_form_main_function':
        html += "<input type='text' id='is_async_{functionName}' name='is_async_{functionName}' value='true' style='display: none;'>".format(
            functionName=Config.getConfig(parentKey='modules', key=mod, subkey=config_subkey)['__function__'])

    footer += '</div>'
    html += footer
    html += '</div>'

    for m in m_form:
        if '__async__' == m and m_form[m] == True:
            async_script = "<script> $(function() { "
            async_script += "$('#{submit_id}').click(function(e)".format(
                submit_id=submit_id)
            async_script += "{ e.preventDefault();"
            async_script += "$.ajax({"
            async_script += "headers: { 'X-CSRFToken': '{"
            async_script += "{csrf_token"
            async_script += "}"
            async_script += "}' }, "
            async_script += "cache: false, contentType: false, processData: false, "
            if config_extrasubkey:
                async_script += "url : '/modules/{mod}/{functionName}/', type : 'POST', async: true, data: $('#form_{mod}_{functionName}').serializeArray(), ".format(
                    mod=mod, functionName=config_extrasubkey)
            else:
                async_script += "url : '/modules/{mod}/{mod}/', type : 'POST', async: true, data: $('#form_{mod}').serializeArray(), ".format(
                    mod=mod)
            async_script += "success : function(res) {"
            async_script += "if('data' in res){"
            async_script += "alert(res.data)"
            async_script += "} else { "
            async_script += "alert('Error')"
            async_script += "}"
            async_script += "}, error : function(xhr,errmsg,err) { console.log(xhr.status + ': ' + xhr.responseText); } }); }); }); </script>"
            html += async_script

    if config_subkey == 'django_form_main_function':
        return {functionModal: html}
    return html


def __getModulesDjangoFormsModal__(session_id=None):
    forms = {}
    for mod in ht.getModulesNames():
        mod_data = {}
        functions = __getModuleFunctionNamesFromConfig__(mod)
        if functions:
            for functs in functions:
                form = __createHtmlModalForm__(
                    mod, 'django_form_module_function', functs, session_id)
                if form:
                    mod_data[functs] = form
        if mod_data:
            forms[mod] = mod_data
    return forms


def __getModuleFunctionNamesFromConfig__(mod):
    functions = ht.Config.getConfig(
        parentKey='modules', key=mod, subkey='django_form_module_function')
    if functions:
        return [func_name for func_name in functions]
    else:
        return

# End Core
