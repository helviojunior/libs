#region Copyright and License
// Copyright 2010..2018 Helvio Junior (https://www.helviojunior.com.br/)
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//   http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#endregion

using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using System.Net;

namespace HelvioJunior.Net.Common
{
    /// <summary>
	///   IPv4 Network class for extends the <see cref="IPAddress" /> class
	/// </summary>
    public class IPNetwork : IPAddress
    {
        private IPAddress _netmask;
        private IPAddress _subnetIP;
        private IPAddress _broadcastIP;
        private Int32 _bitsOfMask;

        public IPAddress Netmask { get { return _netmask; } }

        public IPAddress NetIP { get { return _subnetIP; } }
        public IPAddress BroadcastIP { get { return _broadcastIP; } }
        public Int32 BitsOfMask { get { return _bitsOfMask; } }

        /// <summary>
		///   Parse an IP and CIRD text.
        ///   Ex.: 192.168.0.0/24
		/// </summary>
		/// <param name="text"> IP/CIRD text address, that should be parsed </param>
		/// <returns> New instance of IPNetwork </returns>
        static public IPNetwork Parse(String text)
        {
            String[] txt = text.Split("/".ToCharArray());

            IPAddress ip = null;
            try
            {
                ip = IPAddress.Parse(txt[0]);
            }
            catch
            {
                IPAddress[] tmp = Dns.GetHostAddresses(txt[0]);
                if (tmp.Length > 0)
                    ip = tmp[0];
            }

            if (txt.Length == 0)
            {
                return new IPNetwork(ip.ToString(), 32);
            }
            else
            {
                return new IPNetwork(ip.ToString(), Int32.Parse(txt[1]));
            }
        }

        /// <summary>
		///   New instance of IPNetwork using spfText and bits of mask.
		/// </summary>
		/// <param name="spfText"> SPF Text </param>
        /// <param name="spfText"> Bits of mask </param>
        public IPNetwork(String spfText, Int32 bitOfMask)
            : base(IPAddress.Parse(spfText).Address)
        {
            Int32 desl = (32 - bitOfMask);
            Int64 fullMask = Int64.Parse("4294967295");
            Int64 tmp = ((Int64)(fullMask >> desl)) << desl;
            String[] ip = new IPAddress(tmp).ToString().Split(".".ToCharArray());
            _netmask = IPAddress.Parse(ip[3] + "." + ip[2] + "." + ip[1] + "." + ip[0]);
            Calcule();
        }

        /// <summary>
		///   New instance of IPNetwork using byte array of an Int64 ip addr and byte array of an Int64 ip addr of mask.
		/// </summary>
		/// <param name="address"> Byte array of an Int64 ip addr </param>
        /// <param name="netmask"> byte array of an Int64 ip addr of mask </param>
        public IPNetwork(Byte[] address, Byte[] netmask)
            : base(address)
        {
            _netmask = new IPAddress(netmask);
            Calcule();
        }

        /// <summary>
		///   New instance of IPNetwork using Int64 ip addr and Int64 ip addr of mask.
		/// </summary>
		/// <param name="address"> Int64 ip addr </param>
        /// <param name="netmask"> Int64 ip addr of mask </param>
        public IPNetwork(Int64 address, Int64 netmask)
            : base(address)
        {
            _netmask = new IPAddress(netmask);
            Calcule();
        }

        /// <summary>
		///   New instance of IPNetwork using IPAddress instance of ip addr and IPAddress instance of ip addr of mask.
		/// </summary>
		/// <param name="address"> IPAddress ip addr </param>
        /// <param name="netmask"> IPAddress ip addr of mask </param>
        public IPNetwork(IPAddress address, IPAddress netmask)
            : base(address.Address)
        {
            _netmask = netmask;
            Calcule();
        }

        /// <summary>
		///   New instance of IPNetwork using IPAddress instance of ip addr and CIDR bits of mask.
		/// </summary>
		/// <param name="address"> IPAddress ip addr </param>
        /// <param name="bitOfMask"> CIDR bits of mask (1-32) </param>
        public IPNetwork(IPAddress address, Int32 bitOfMask)
            : base(address.Address)
        {
            Int32 desl = (32 - bitOfMask);
            Int64 fullMask = Int64.Parse("4294967295");
            Int64 tmp = ((Int64)(fullMask >> desl)) << desl;
            String[] ip = new IPAddress(tmp).ToString().Split(".".ToCharArray());
            _netmask = IPAddress.Parse(ip[3] + "." + ip[2] + "." + ip[1] + "." + ip[0]);
            Calcule();
        }

        /// <summary>
		///   Get String nottation of Network ip/cidr.
		/// </summary>
        public String ToString()
        {
            return this._subnetIP.ToString() + "/" + this._bitsOfMask;
        }
        
        /// <summary>
		///   Compare if an IP address is member of this network.
		/// </summary>
		/// <param name="address"> IPAddress to check </param>
        public Boolean Compare(IPAddress address)
        {
            Int64 i1 = (Int64)address.Address;
            Int64 i2 = (Int64)_netmask.Address;

            return (new IPAddress(i1 & i2).ToString() == _subnetIP.ToString());
        }

        /// <summary>
		///   Get an list of all usable hosts of this network.
        ///   Excluding net address and broadcast address.
		/// </summary>
		/// <param name="address"> IPAddress to check </param>
        public List<IPAddress> GetHostAddrList()
        {
            List<IPAddress> hosts = new List<IPAddress>();

            Int32[] netIP = GetOctets(this.NetIP);
            Int32[] broadcatIP = GetOctets(this.BroadcastIP);

            for (Int32 o1 = netIP[0]; o1 <= broadcatIP[0]; o1++)
            {
                for (Int32 o2 = netIP[1]; o2 <= broadcatIP[1]; o2++)
                {
                    for (Int32 o3 = netIP[2]; o3 <= broadcatIP[2]; o3++)
                    {
                        for (Int32 o4 = netIP[3]; o4 <= broadcatIP[3]; o4++)
                        {
                            IPAddress tmp = IPAddress.Parse(o1 + "." + o2 + "." + o3 + "." + o4);
                            if ((tmp.ToString() != _subnetIP.ToString()) && (tmp.ToString() != _broadcastIP.ToString()))
                                hosts.Add(IPAddress.Parse(o1 + "." + o2 + "." + o3 + "." + o4));
                        }
                    }
                }
            }

            return hosts;
        }

        /// <summary>
		///   Get all subnet network addresses of an CIDR.
		/// </summary>
		/// <param name="bitsOfMask"> Bits of mask to convert this network </param>
        public List<IPNetwork> GetSubnetsAddrList(Int32 bitsOfMask)
        {
            if (bitsOfMask <= this.BitsOfMask)
                throw new Exception("Bits of mask need be lower than local bits of mask");

            List<IPNetwork> subnets = new List<IPNetwork>();

            IPNetwork subnet = new IPNetwork(this, bitsOfMask);
            while (subnet != null)
            {
                subnets.Add(subnet);

                IPAddress nextSubnetIP = GetNextIpAddress(subnet.BroadcastIP);
                if (this.Compare(nextSubnetIP))
                    subnet = new IPNetwork(nextSubnetIP, bitsOfMask);
                else
                    subnet = null;

            } 

            return subnets;
        }

        private IPAddress GetNextIpAddress(IPAddress ipAddress)
        {
            byte[] addressBytes = ipAddress.GetAddressBytes().Reverse().ToArray();
            uint ipAsUint = BitConverter.ToUInt32(addressBytes, 0);
            var nextAddress = BitConverter.GetBytes(ipAsUint + 1);
            return IPAddress.Parse(String.Join(".", nextAddress.Reverse()));
        }

        public Int32[] GetOctets(IPAddress ip)
        {
            String[] o1 = ip.ToString().Split(".".ToCharArray());
            Int32[] ret = new Int32[o1.Length];

            ret[0] = Int32.Parse(o1[0]);
            ret[1] = Int32.Parse(o1[1]);
            ret[2] = Int32.Parse(o1[2]);
            ret[3] = Int32.Parse(o1[3]);

            return ret;
        }

        
        private IPAddress GetBroadcastAddress(IPAddress address, IPAddress subnetMask)
        {
            byte[] ipAdressBytes = address.GetAddressBytes();
            byte[] subnetMaskBytes = subnetMask.GetAddressBytes();

            if (ipAdressBytes.Length != subnetMaskBytes.Length)
                throw new ArgumentException("Lengths of IP address and subnet mask do not match.");

            byte[] broadcastAddress = new byte[ipAdressBytes.Length];
            for (int i = 0; i < broadcastAddress.Length; i++)
            {
                broadcastAddress[i] = (byte)(ipAdressBytes[i] | (subnetMaskBytes[i] ^ 255));
            }
            return new IPAddress(broadcastAddress);
        }

        
        private void Calcule()
        {
            Int64 i1 = (Int64)this.Address;
            Int64 i2 = (Int64)_netmask.Address;

            this._bitsOfMask = CountBit(_netmask.Address.ToString());

            this._subnetIP = new IPAddress(i1 & i2);

            Int32 tst = this._bitsOfMask ^ int.MinValue;

            this._broadcastIP = GetBroadcastAddress(this, _netmask);
        }

        private Int32 CountBit(string mask)
        {

            int ones = 0;
            Array.ForEach(mask.Split('.'), (s) => Array.ForEach(Convert.ToString(Int64.Parse(s), 2).Where(c => c == '1').ToArray(), (k) => ones++));
            return ones;

        }

    }
}
