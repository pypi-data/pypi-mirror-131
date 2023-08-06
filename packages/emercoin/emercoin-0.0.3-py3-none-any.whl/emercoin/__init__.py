import emercoin.models as models
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


class Emer:
    def __init__(
        self, user: str, password: str, host: str = "localhost", port: int = 6662
    ):
        self.rpc_connection = AuthServiceProxy(
            f"http://{user}:{password}@{host}:{str(port)}"
        )

    def get_block_count(self) -> int:
        return self.rpc_connection.getblockcount()

    def name_show(self, name: (str, models.NVSRecord)) -> models.NVSTx:
        if isinstance(name, models.NVSRecord):
            name = name.name
        r = self.rpc_connection.name_show(name)
        record = models.NVSRecord(name, r["value"])
        tx = models.Transaction(r["txid"], r["time"])
        addr = models.EmcAddress(r["address"])
        return models.NVSTx(record, addr, tx)

    def name_filter(self, regexp: str) -> [models.NVSRecord]:
        r = self.rpc_connection.name_filter(regexp)
        resp: [models.NVSRecord] = []
        for i in r:
            resp.append(models.NVSRecord(name=i["name"], value=i["value"]))
        return resp

    def name_history(self, name: (str, models.NVSRecord)) -> [models.NVSTx]:
        if isinstance(name, models.NVSRecord):
            name = name.name
        r: [{}] = self.rpc_connection.name_history(name)
        ret: [models.NVSTx] = []
        for i in r:
            record = models.NVSRecord(name, i["value"])
            tx = models.Transaction(i["txid"], i["time"], i["height"])
            addr = models.EmcAddress(i["address"])
            days = i["days_added"]
            ret.append(models.NVSTx(record, addr, tx, days))
        return ret

    def get_names_by_type(self, type: str) -> [models.NVSTx]:
        l = self.name_filter(f"^{type}:")
        ret: [models.NVSTx] = []
        for n in l:
            try:
                ret.append(self.name_show(n))
            except JSONRPCException:
                continue
        return ret

    def get_names_by_regex(self, regex: str) -> [models.NVSTx]:
        l = self.name_filter(regex)
        ret: [models.NVSTx] = []
        for n in l:
            try:
                ret.append(self.name_show(n))
            except JSONRPCException:
                continue
        return ret
