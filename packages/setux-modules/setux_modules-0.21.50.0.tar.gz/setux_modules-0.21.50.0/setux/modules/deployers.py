from setux.core.deploy import Deployers, Deployer
from setux.core.deployers import Sender
from setux.managers.common.user.deployers import User_


class Sudoer(Deployer):
    '''Add User to sudoers

    context:
        user : user name
    '''

    @property
    def label(self):
        return f'Sudoer {self.user}'

    def check(self):
        grp = self.target.groups.fetch(self.user)
        ok = 'wheel' in grp.get()

        ret, out, err = self.target.run(f'sudo -l -U {self.user}')
        ok = ok and '(ALL) NOPASSWD: ALL' == out[-1].strip()
        return ok

    def deploy(self):
        grp = self.target.groups.fetch(self.user)
        grp.add('wheel')

        ok = self.target.write(
            f'/etc/sudoers.d/{self.user}',
            f'{self.user} ALL=(ALL) NOPASSWD: ALL',
        )
        return ok


class CopyId(Deployer):
    '''Send Public Key to Target
    context:
        user : User name
        pub  : Public key
    '''

    @property
    def label(self):
        return f'Copy ID {self.user}'

    def check(self):
        user = self.target.user.fetch(self.user)
        if user.check() is not True: return False

        path = f'/home/{self.user}/.ssh/authorized_keys'
        pub = self.target.file.fetch(
            path, mode='600', user=self.user, group=user.group.name
        )
        return pub.check() is True

    def deploy(self):
        user = self.target.user.fetch(self.user)

        path = f'/home/{self.user}/.ssh'
        ssh = self.target.dir(
            path, mode='700', user=self.user, group=user.group.name
        )
        if ssh.check() is not True: return False

        full = f'{path}/authorized_keys'
        sent = Sender(self.target, src=self.pub, dst=full, **self.context)()
        if sent is not True: return False

        key = self.target.file(
            full, mode='600', user=self.user, group=user.group.name
        )
        return key.check() is True


class Admin(Deployers):
    '''Set User as sudoer
    context:
        user : User name
        pub  : Public key

    - Create User if not present
    - Add User to sudoers
    - Send User's public key
    '''

    @property
    def label(self):
        return f'Admin {self.user}'

    @property
    def deployers(self):
        return [
            User_,
            Sudoer,
            CopyId,
        ]

