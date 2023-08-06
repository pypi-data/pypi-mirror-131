def printit():
    print("""
    
    
    
    //server 
    import java.net.*;
    import java.util.Scanner;
    import java.io.*;
    
    public class Server {
        public static void main(String[] args) {
            try {
                ServerSocket se = new ServerSocket(1537);
                
                System.out.println("Server waiting");
                
                Socket server = se.accept();
                
                System.out.println("Connection established");
                Scanner sc = new Scanner(server.getInputStream());
                String filename = sc.nextLine();
                
                FileReader f = null;
                Scanner ff = null;
                DataOutputStream sendToClient = new DataOutputStream(server.getOutputStream());
                File file = new File(filename);
                
                if (file.exists()) {
                    sendToClient.writeBytes("Yes\n");
                    f = new FileReader(filename);
                    ff = new Scanner(f);
                    String string;
                    while ((string = ff.next()) != null)
                        sendToClient.writeBytes(string + "\n");
                } else {
                    sendToClient.writeBytes("No\n");
                }
                server.close();
                sc.close();
                sendToClient.close();
                f.close();
                ff.close();
                se.close();
            } catch (Exception ex) {
            }
        }
    }
    
    
    //client
    import java.net.*;
    import java.util.Scanner;
    import java.io.*;
    
    public class Client {
        public static void main(String[] args) {
            try {
                Socket client = new Socket("localhost", 1537);
                Scanner sc = new Scanner(System.in);
                System.out.println("Enter file location:");
                String filename = sc.nextLine();
                DataOutputStream sendToServer = new DataOutputStream(client.getOutputStream());
                sendToServer.writeBytes(filename + "\n");
                Scanner i =  new Scanner(client.getInputStream());
                String string = i.nextLine();
                if (string.equals("Yes")) {
                    while ((string = i.next()) != null)
                        System.out.println(string);
                } else
                    System.out.println("File not found");
                sc.close();
                client.close();
                sendToServer.close();
                i.close();
            } catch (Exception ex) {
            }
        }
    }
    
    
    
    """)