import socket
import subprocess
from Tests.commFunctions import CheckPingAllAngles

class sendCmd:
    def __init__(self):
        self.all_ips = []
        self.mac = "00:0C:29:A4:AD:FB"

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()

    def lookVimIp(self):
        proc = subprocess.check_output("arp -a" ).decode('utf-8')
        ip_prefix = "192.168.192"
        while ip_prefix in proc:
            ip_place = proc.find(ip_prefix)
            ip_length = 15
            ip = proc[ip_place:ip_place+ip_length]
            #print(ip)
            self.all_ips.append(ip)
            proc = proc[ip_place+ip_length:]

        #print (self.all_ips)


    def getVimIpPing(self):
        if len(self.all_ips) > 2:
            for s_ip in self.all_ips[1:]:
                pingR = CheckPingAllAngles(s_ip, 3)
                #print(pingR)
                if pingR != -1:
                    return s_ip
        else:
            return "Not enough ips were found. restart the ViM."


if __name__ == "__main__":
    myCmd = sendCmd()
    myCmd.lookVimIp()
    print(myCmd.getVimIpPing())
