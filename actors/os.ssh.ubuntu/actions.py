def install (job):
    service = job.service
    if 'sshkey' not in service.producers:
        raise j.exceptions.AYSNotFound("No sshkey service consumed. please consume an sshkey service")
    service.logger.info("authorize ssh key to machine")
    node = service.parent
    ssh_port = '22'
    for parent in service.parents:
        if parent.model.role != 'node':
            continue
        for port in parent.model.data.ports:
            src, _, dst = port.partition(':')
            if ssh_port == dst:
                ssh_port = src
                break
    service.model.data.sshPort = int(ssh_port)
    sshkey = service.producers['sshkey'][0]
    key_path = sshkey.model.data.keyPath
    if not j.sal.fs.exists(key_path):
        raise j.exceptions.RuntimeError("sshkey path not found at %s" % key_path)
    password = node.model.data.sshPassword if node.model.data.sshPassword != '' else None
    passphrase = sshkey.model.data.keyPassphrase if sshkey.model.data.keyPassphrase != '' else None
    executor = j.tools.executor.getSSHBased(addr=node.model.data.ipPublic, port=service.model.data.sshPort,
                                            login=node.model.data.sshLogin, passwd=password,
                                            allow_agent=True, look_for_keys=True, timeout=5, usecache=False,
                                            passphrase=passphrase, key_filename=key_path)
    executor.prefab.system.ssh.authorize("root", sshkey.model.data.keyPub)
    j.tools.prefab.resetAll()
    service.saveAll()
    

def getExecutor (job):
    service = job.service
    if 'sshkey' not in service.producers:
        raise j.exceptions.AYSNotFound("No sshkey service consumed. please consume an sshkey service")
    sshkey = service.producers['sshkey'][0]
    node = service.parent
    key_path = sshkey.model.data.keyPath
    passphrase = sshkey.model.data.keyPassphrase if sshkey.model.data.keyPassphrase != '' else None
    ssh_port = '22'
    for parent in service.parents:
        if parent.model.role != 'node':
            continue
        for port in parent.model.data.ports:
            src, _, dst = port.partition(':')
            if ssh_port == dst:
                ssh_port = src
                break
    executor = j.tools.executor.getSSHBased(addr=node.model.data.ipPublic, port=ssh_port,
                                            login='root', passwd=None,
                                            allow_agent=True, look_for_keys=True, timeout=5, usecache=False,
                                            passphrase=passphrase, key_filename=key_path)
    return executor
    

def input (job):
    return None
    

def init (job):
    pass
    

def stop (job):
    pass
    

def start (job):
    pass
    

def monitor (job):
    pass
    

def halt (job):
    pass
    

def check_up (job):
    pass
    

def check_down (job):
    pass
    

def check_requirements (job):
    pass
    

def cleanup (job):
    pass
    

def data_export (job):
    pass
    

def data_import (job):
    pass
    

def uninstall (job):
    pass
    

def removedata (job):
    pass
    

def consume (job):
    pass
    

def action_pre_ (job):
    pass
    

def action_post_ (job):
    pass
    

def init_actions_ (service, args):
    '''
    this needs to returns an array of actions representing the depencies between actions.
Looks at ACTION_DEPS in this module for an example of what is expected

    '''
    
    # some default logic for simple actions
    
    action_required = args.get('action_required')
    
    if action_required in ['stop', 'uninstall']:
        for action_name, action_model in service.model.actions.items():
            if action_name in ['stop', 'uninstall']:
                continue
            if action_model.state == 'scheduled':
                action_model.state = 'new'
    
    if action_required in ['install']:
        for action_name, action_model in service.model.actions.items():
            if action_name in ['uninstall', 'stop'] and action_model.state == 'scheduled':
                action_model.state = 'new'
    
    
    if action_required == 'stop':
        if service.model.actionsState['start'] == 'sheduled':
            service.model.actionsState['start'] = 'new'
    
    if action_required == 'start':
        if service.model.actionsState['stop'] == 'sheduled':
            service.model.actionsState['stop'] = 'new'
    
    service.save()
    
    return {
        'init': [],
        'install': ['init'],
        'start': ['install'],
        'monitor': ['start'],
        'stop': [],
        'delete': ['uninstall'],
        'uninstall': ['stop'],
    }
    
    

def delete (job):
    job.service.delete()
    

