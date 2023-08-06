from setux.core.deploy import Deployers, Deployer


class User_(Deployer):
    @property
    def label(self):
        return 'user'

    def check(self):
        ret, out, err = self.target.run(f'which {self.shell}')
        shell = out[0]
        usr = self.target.user.fetch(self.user,
            uid   = self.uid,
            gid   = self.gid,
            shell = shell,
            home  = f'/home/{self.user}',
        )
        ok = usr.check() is True
        if not ok: return False
        ok = usr.home.check() is True
        return ok

    def deploy(self):
        ret, out, err = self.target.run(f'which {self.shell}')
        shell = out[0]
        usr = self.target.user.fetch(self.user,
            uid   = self.uid,
            gid   = self.gid,
            shell = shell,
            home  = f'/home/{self.user}',
        )
        return usr.deploy() is True


class Groups(Deployer):
    @property
    def label(self):
        return 'groups'

    def check(self):
        grp = self.target.groups.fetch(self.user, *self.groups.split())
        return grp.check() is True

    def deploy(self):
        grp = self.target.groups.fetch(self.user, *self.groups.split())
        return grp.deploy() is True


class User(Deployers):
    @property
    def label(self):
        return f'User {self.user}'

    @property
    def deployers(self):
        return [
            User_,
            Groups,
        ]

