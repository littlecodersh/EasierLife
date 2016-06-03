__all__ = ['ApiFramework']

__API_LIST = {
    'document':{
        'get': 'Get document',
    },
}
class ApiError(AttributeError):
    def __init__(self, path):
        self.message = "api has no attribute '%s'"%'.'.join(path)
        self.args = (self.message,)
class ApiFramework(object):
    def __init__(self, apiList = {}, warning = False, path = []):
        self.apiList = apiList
        self.warning = apiList != {} and warning
        self.path = path
    def __getattr__(self, s):
        try:
            tmpApi = self.apiList
            for name in self.path + [s]: tmpApi = tmpApi[name]
        except:
            if self.warning: raise ApiError(self.path + [s])
            api = ApiFramework(self.apiList, self.warning, self.path + [s])
        else:
            api = ApiFramework(self.apiList, self.warning, self.path + [s])
            api.__doc__ = tmpApi
        return api
    def __call__(self, *args, **kwargs):
        return self.path

if __name__ == '__main__':
    api = ApiFramework(__API_LIST, True)
    print(api.document.get())
    print(api.document.send())
