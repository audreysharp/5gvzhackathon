import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.URL;
import java.util.ArrayList;
import java.util.Scanner;

class CSV{
    protected ArrayList<String[]> lines = new ArrayList<String[]>();
    public CSV(String url) throws FileNotFoundException{
        File f = new File(url);
        Scanner scan = new Scanner(f);
        while(scan.hasNextLine()){
            String line = scan.nextLine();
            addLine(line);
        }
        scan.close();
    }
    public void addLine(String line){
        lines.add(line.split(","));
    }
    public String getInfo(int n){
        return this.getID(n) + ", "+ this.getLatitude(n) + ", "+  this.getLongitude(n);
    }
    public String getID(int n){
        return lines.get(n)[0];
    }
    public String getLatitude(int n){
        return lines.get(n)[2];
    }
    public String getLongitude(int n){
        return lines.get(n)[3];
    }
    public Double getDistance(CSV d, int a, int b){
        return getD(this.getLatitude(a),this.getLongitude(a),d.getLatitude(b),d.getLongitude(b));
    }
    public static double getD(String la1,String lo1,String la2,String lo2){
        double R = 6373;
        double km2ft = 3280.84;

        double lat1 = Double.parseDouble(la1);
        double lon1 = Double.parseDouble(lo1);
        double lat2 = Double.parseDouble(la2);
        double lon2 = Double.parseDouble(lo2);

        double dlon = Math.toRadians(lon2 - lon1);
        double dlat = Math.toRadians(lat2 - lat1);
        double a = Math.pow((Math.sin(dlat/2)),2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow((Math.sin(dlon/2)),2);
        double c = 2 * Math.atan2( Math.sqrt(a), Math.sqrt(1-a) );
        double d = R * c;

        return (d*km2ft);
    }
}

class Test{
    public static ArrayList<String> city =  new ArrayList<String>();
    public static int totalhouses = 0;

    public static void test(CSV a, CSV h, PrintWriter pw,int T){
        ArrayList<ArrayList<String>> antenna = new ArrayList<ArrayList<String>>();
        int maxHouse = 0;
        int indexA = 0;
        for(int i = 0; i<a.lines.size(); i++){
            ArrayList<String> line = new ArrayList<String>();
            int myHouse = 0;
            for(int j = 0; j<h.lines.size(); j++){
                if(!(city.contains(h.getID(j)))){continue;}
                if(a.getDistance(h,i,j) <= T){
                    line.add(h.getID(j));
                    myHouse++;
                }
            }
            if(myHouse > maxHouse){
                maxHouse = myHouse;
                indexA = i;
            }
            antenna.add(line);
        }
        String tstr = "";
        switch(T){
            case 100:
                tstr = "T-1";
                break;
            case 200:
                tstr = "T-2";
                break;
            case 300:
                tstr = "T-3";
                break;
            case 400:
                tstr = "T-4";
                break;
            case 500:
                tstr = "T-5";
                break;
        }
        pw.println(a.getID(indexA) +","+ tstr);
        System.out.println(a.getID(indexA) + "\t" + tstr + "\t" + (totalhouses += antenna.get(indexA).size()));

        for(String line : antenna.get(indexA)){
            if(city.contains(line)){
                city.remove(line);
            }
        }
    }
    public static void main(String[] args) throws FileNotFoundException {
        CSV house = new CSV("./houseList.csv");
        CSV antenna = new CSV("./antennaLocations.csv");

        //System.out.println(antenna.getDistance(house, 0, 2));

        for (int i = 0; i < house.lines.size(); i++) {
            city.add(house.getID(i));
        }

        File f = new File("./output.csv");
        PrintWriter pw = new PrintWriter(f);
        pw.println("AntennaLocationCode,AntennaType");

        for (int i = 0; i < 35; i++)
            test(antenna, house, pw, 500);
        for (int i = 0; i < 0; i++)
            test(antenna, house, pw, 400);
        for (int i = 0; i < 40; i++) {
            test(antenna, house, pw, 300);
        }
        for (int i = 0; i < 0; i++) {
            test(antenna, house, pw, 200);
        }
        for (int i = 0; i < 30; i++) {
            test(antenna, house, pw, 100);
        }
        pw.close();
        System.out.println("DONE - Total: " + totalhouses);
    }
}