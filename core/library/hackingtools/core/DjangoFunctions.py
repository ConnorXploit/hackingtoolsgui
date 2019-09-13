from core.library import hackingtools as ht
from . import Config, Logger, Utils
Logger.setDebugModule(True)

from colorama import Fore
import os

config_locales = Config.getConfig(parentKey='core', key='locales')

def createModuleFunctionView(moduleName, functionName):
    Logger.printMessage(message='Creating Function Modal View', description=functionName, debug_module=True)
    # Creates the JSON config for the view modal form
    category = ht.getModuleCategory(moduleName)
    functionParams = Utils.getFunctionsParams(category=category, moduleName=moduleName, functionName=functionName)
    moduleViewConfig = {}

    moduleViewConfig['__function__'] = functionName
    moduleViewConfig['__async__'] = False
    if Utils.doesFunctionContainsExplicitReturn(Utils.getFunctionFullCall(moduleName, functionName)):
        moduleViewConfig['__return__'] = 'text'
    else:
        moduleViewConfig['__return__'] = False
    if functionParams:
        if 'params' in functionParams:
            for param in functionParams['params']:
                moduleViewConfig[param] = {}
                moduleViewConfig[param]['__type__'] = 'text'
                moduleViewConfig[param]['label_desc'] = param
                moduleViewConfig[param]['placeholder'] = param
                moduleViewConfig[param]['required'] = True

        if 'defaults' in functionParams:
            for param in functionParams['defaults']:
                moduleViewConfig[param] = {}
                moduleViewConfig[param]['__type__'] = Utils.getValueType(functionParams['defaults'][param])
                moduleViewConfig[param]['label_desc'] = param
                moduleViewConfig[param]['placeholder'] = param
                moduleViewConfig[param]['value'] = functionParams['defaults'][param]

    Config.__save_django_module_config__(moduleViewConfig, category, moduleName, functionName)
    return {functionName : moduleViewConfig}

def getModulesGuiNames():
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
        label = Config.getConfig(parentKey='modules', key=tool, subkey='__gui_label__')
        if label:
            names[tool] = label
    return names

def getModulesModalTests():
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
        tool_functions = Config.getConfig(parentKey='modules', key=tool, subkey='django_form_module_function')
        if tool_functions:
            tools_functions[tool] = tool_functions
    return tools_functions

def getModulesFunctionsCalls():
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
    header = 'import hackingtools as ht\n\nht_mod = ht.getModule("{module_name}")\nmod_result = ht_mod.{module_function}({module_function_params})\n\nprint(mod_result)'
    for module in ht.modules_loaded:
        module_funcs = {}
        for func in ht.modules_loaded[module]:
            try:
                for param in ht.modules_loaded[module][func]:
                    module_funcs[func] = header.format(module_name=module.split('.')[-1], module_function=func, module_function_params=', '.join(ht.modules_loaded[module][func][param]))
            except:
                module_funcs[func] = header.format(module_name=module.split('.')[-1], module_function=func, module_function_params='')
        modulesCalls[module.split('.')[-1]] = module_funcs
    return modulesCalls

def __getModulesConfig_treeView__():
    """Return a String with the config for the GUI Treeview

    Parameters
    ----------
        None

    Return
    ----------
        String
    """
    count = 1
    result_text = []
    tools_config = ht.getModulesFullConfig()
    __treeview_load_all__(config=tools_config, result_text=result_text)
    response =  ','.join(result_text)
    return response

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
    open_key = "{"
    close_key = "}"
    count += 1
    count_pid += 1
    for c in config:
        count += 1
        count = __treeview_count__(count)
        result_text.append(__treeview_createJSON__(conf_key=config[c], key=c, count=count, pid=count_pid))
        Logger.printMessage('{msg} - {key} - {n} - {m}'.format(msg='Pasando por: ', key=c, n=count, m=count_pid), color=Fore.YELLOW, debug_core=True)
        if not isinstance(config[c], str) and not isinstance(config[c], bool) and not isinstance(config[c], int) and not isinstance(config[c], float):
            try:
                __treeview_load_all__(config=config[c],result_text=result_text, count=count, count_pid=count-1)
                count += 1
            except:
                try:
                    __treeview_load_all__(config=tuple(config[c]),result_text=result_text, count=count, count_pid=count-1)
                    count += 1
                    Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=config_locales['error_json_data_loaded'], key=c, conf_key=config[c]), color=Fore.YELLOW, debug_core=True)
                except:
                    Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=config_locales['error_json_data_not_loaded'], key=c, conf_key=config[c]), color=Fore.RED, debug_core=True)
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
        Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=config_locales['error_load_json_data'], key=key, conf_key=conf_key), color=Fore.RED)

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

def __createHtmlModalForm__(mod, config_subkey='django_form_main_function', config_extrasubkey=None):
    module_form = Config.getConfig(parentKey='modules', key=mod, subkey=config_subkey, extrasubkey=config_extrasubkey)
    functionModal = Config.getConfig(parentKey='modules', key=mod, subkey=config_subkey, extrasubkey='__function__')
    default_classnames_per_type = Config.getConfig(parentKey='django', key='html', subkey='modal_forms', extrasubkey='default_types')
    if not module_form:
        return
    
    html = "<div class=\"modal-body\">"
    footer = '<div class="modal-footer">'
    m_form = module_form

    # For ajax
    submit_id = ''

    if '__function__' in m_form:
        submit_id = 'submit_{mod}_{name}'.format(mod=mod, name=m_form['__function__'])

    for m in m_form:
        temp_m_form = m_form
        if not m == '__async__' and not m == '__function__' and not '__separator' in m and (('systems' in temp_m_form[m] and os.name in temp_m_form[m]['systems']) or not 'systems' in temp_m_form[m]):
            if '__type__' in temp_m_form[m]:
                input_type = temp_m_form[m]['__type__']
                
                input_className = ''
                if not input_type in default_classnames_per_type:
                    Logger.printMessage(message='__createHtmlModalForm__', description='There is no __className__ defined for this type of input \'{input_type}\''.format(input_type=input_type), color=Logger.Fore.YELLOW)
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
                
                checkbox_selected = False
                if 'selected' in temp_m_form[m]:
                    checkbox_selected = temp_m_form[m]['selected']
                
                loading_text = ''
                if 'loading_text' in temp_m_form[m]:
                    loading_text = temp_m_form[m]['loading_text']
                
                required = ''
                if 'required' in temp_m_form[m] and temp_m_form[m]['required'] == True:
                    required = 'required'
                
                options_from_function = []
                if 'options_from_function' in temp_m_form[m]:
                    options_from_function = temp_m_form[m]['options_from_function']
                    for optModuleName in options_from_function:
                        if optModuleName in ht.getModulesNames():
                            functionCall = 'ht.getModule(\'{mod}\').{func}()'.format(mod=optModuleName, func=temp_m_form[m]['options_from_function'][optModuleName])
                            options_from_function = eval(functionCall)
                        if 'core' == optModuleName:
                            functionCall = 'ht.{func}()'.format(func=temp_m_form[m]['options_from_function'][optModuleName])
                            options_from_function = eval(functionCall)

                if input_type == 'file':
                    #html += "<label class=\"btn btn-default\">{input_label_desc}<span class=\"name-file\"></span><input type=\"file\" name=\"{id}\" class=\"{className}\" hidden {required} /></label>".format(input_label_desc=input_label_desc, className=input_className, id=m, required=required)
                    html += "<div class='input-group'>"
                    html += "<div class='input-group-prepend'>"
                    html += "<span class='input-group-text' id='inputGroupFileAddon01{id}'>{input_label_desc}</span>".format(id=m, input_label_desc=input_label_desc)
                    html += "</div>"
                    html += "<div class='custom-file'>"
                    html += "<input type='file' class='custom-file-input' name='{id}' aria-describedby='inputGroupFileAddon01{id}' {required}>".format(id=m, required=required)
                    html += "<label class='custom-file-label' for='{id}'>Choose file</label>".format(id=m)
                    html += "</div>"
                    html += "</div>"

                elif input_type == 'checkbox':
                    checkbox_disabled = ''
                    color_on = 'primary'
                    color_off = 'warning'
                    
                    
                    if '__pool_it_' in m and not ht.WANT_TO_BE_IN_POOL:
                        checkbox_disabled = 'disabled'
                        color_on = 'default'
                        color_off = 'default'
                    
                    if checkbox_selected:
                        html += "<div class=\"checkbox\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"{color_on}\" data-offstyle=\"{color_off}\" id=\"{id}\" name=\"{id}\" {required} checked {disabled}><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></div><br />".format(color_on=color_on, color_off=color_off, id=m, input_label_desc=input_label_desc, required=required, disabled=checkbox_disabled)
                    else:
                        html += "<div class=\"checkbox\"><input type=\"checkbox\" class=\"checkbox\" data-toggle=\"toggle\" data-on=\"On\" data-off=\"Off\" data-onstyle=\"{color_on}\" data-offstyle=\"{color_off}\" id=\"{id}\" name=\"{id}\" {required} {disabled}><label style=\"padding: 0 10px;\" for=\"{id}\">{input_label_desc}</label></div><br />".format(color_on=color_on, color_off=color_off, id=m, input_label_desc=input_label_desc, required=required, disabled=checkbox_disabled)
                
                elif input_type == 'select':

                    html += "<span class=\"name-select\" value=\"{placeholder}\"></span><select id=\"editable-select-{id}\" name=\"dropdown_{id}\" placeholder=\"{placeholder}\" class=\"{className}\" {required}>".format(placeholder=input_placeholder, className=input_className, id=m, required=required)
                    html += "<option value='{input_value}' selected></option>".format(input_value=input_value)

                    for func in options_from_function:
                        html += "<option value='{cat}'>{cat}</option>".format(cat=func)
                    
                    html += "</select><script>$('#editable-select-{id}').editableSelect();".format(id=m)

                    if required != '':
                        html += "$('#editable-select-{id}').prop('required',true);".format(id=m)

                    html += "</script>"

                elif input_type == 'button':

                    footer += "<button type=\"button\" class=\"{className}\" data-dismiss=\"modal\">{input_value}</button>".format(className=input_className, input_value=input_value)

                elif input_type == 'submit':

                    submit_id = m
                    footer += "<input type=\"submit\" class=\"{className}\" value=\"{input_value}\" id=\"{id}\" />".format(className=input_className, input_value=input_value, id=submit_id)
                    
                    if loading_text:
                        footer += "<script>$('#"
                        footer += m
                        footer += "').on('click', function(e){$('#"
                        footer += m
                        footer += "').attr('value', '{loading_text}'); e.preventDevault();".format(loading_text=loading_text)
                        footer += "});</script>"

                elif input_type == 'textarea':

                    if input_label_desc:
                        html += "<div class=\"form-group row\"><label for=\"{id}\" class=\"col-4 col-form-label label-description\">{input_label_desc}</label><div class=\"col-4\"><textarea class=\"{className}\" name=\"{id}\" id=\"{id}\" rows=\"5\" placeholder=\"{placeholder}\"></textarea></div></div>".format(className=input_className, id=m, placeholder=input_placeholder, input_label_desc=input_label_desc)
                    else:
                        html += "<textarea class=\"{className}\" name=\"{id}\" id=\"{id}\" rows=\"5\" placeholder=\"{placeholder}\"></textarea>".format(className=input_className, id=m, placeholder=input_placeholder)

                else:
                    html += "<div class='md-form'><label for=\"{id}\">{input_label_desc}</label><input class=\"{className}\" type=\"{input_type}\" value=\"{input_value}\" placeholder=\"{placeholder}\" name=\"{id}\" {required}/></div>".format(id=m, placeholder=input_placeholder, input_label_desc=input_label_desc, className=input_className, input_type=input_type, input_value=input_value, required=required)

        if '__separator' in m and '__' == m[-2:] and m_form[m] == True:
            html += "<hr class='sidebar-divider my-0 my-separator'>"

    for m in m_form:
        if '__async__' == m and m_form[m]:
            html += "<input type='text' value='true' id='is_async' hidden />"

    footer += '</div>'
    html += footer
    html += '</div>'

    for m in m_form:
        if '__async__' == m and m_form[m] == True:
            async_script = "<script> $(function() { "
            async_script += "$('#{submit_id}').click(function(e)".format(submit_id=submit_id)
            async_script += "{ e.preventDefault();"
            async_script += "$.ajax({"
            async_script += "headers: { 'X-CSRFToken': '{"
            async_script += "{csrf_token"
            async_script += "}"
            async_script += "}' }, "
            async_script += "cache: false, contentType: false, processData: false, "
            if config_extrasubkey:
                async_script += "url : '/modules/{mod}/{functionName}/', type : 'POST', async: true, data: $('#form_{mod}_{functionName}').serializeArray(), ".format(mod=mod, functionName=config_extrasubkey)
            else:
                async_script += "url : '/modules/{mod}/{mod}/', type : 'POST', async: true, data: $('#form_{mod}').serializeArray(), ".format(mod=mod)
            async_script += "success : function(res) {"
            async_script += "if('data' in res){"
            async_script += "alert(res.data)"
            async_script += "} else { "
            async_script += "alert('Error')"
            async_script += "}"
            async_script += "}, error : function(xhr,errmsg,err) { console.log(xhr.status + ': ' + xhr.responseText); } }); }); }); </script>"
            html += async_script
    if config_subkey == 'django_form_main_function':
        return {functionModal : html}
    return html

def __getModulesDjangoFormsModal__():
    forms = {}
    for mod in ht.getModulesNames():
        mod_data = {}
        functions = __getModuleFunctionNamesFromConfig__(mod)
        if functions:
            for functs in functions:
                form = __createHtmlModalForm__(mod, 'django_form_module_function', functs)
                if form:
                    mod_data[functs] = form
        if mod_data:
            forms[mod] = mod_data
    return forms

def __getModuleFunctionNamesFromConfig__(mod):
    functions = Config.getConfig(parentKey='modules', key=mod, subkey='django_form_module_function')
    if functions:
        return [func_name for func_name in functions]
    else:
        return

# End Core