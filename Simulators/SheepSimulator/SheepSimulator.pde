import processing.net.*;
import java.util.regex.*;
import java.util.Iterator;

//Whole Object representation.
Sheep theSheep;
int currentPanel=0;
PShape selectedPanel;
float lastMouseX= 0;
float lastMouseY= 0;
int clickCount = 0;
boolean firstRun = true;
HashMap<Integer, ArrayList<Integer>> partySideMap = new HashMap<Integer, ArrayList<Integer>>();
HashMap<Integer, ArrayList<Integer>> boringSideMap = new HashMap<Integer, ArrayList<Integer>>();

// network vars
int port = 4444;
Server _server; 
StringBuffer _buf = new StringBuffer();

void setup() {
  size(640, 360, P3D);
  theSheep =  new Sheep("simplesheepselectedonly.obj");
  theSheep.sheepModel.rotateX(PI);
  theSheep.sheepModel.rotateY(PI*1.5);

  partySideMap = loadPolyMap("SheepPanelPolyMap.csv", "p");
  boringSideMap = loadPolyMap("SheepPanelPolyMap.csv", "b");
  mousePressed();

  _server = new Server(this, port);
  println("server listening:" + _server);
}

void draw() {
  background(0);

  translate(320, 180);  

  shape(theSheep.sheepModel);

  pollServer();
}




void mouseDragged() {
  if (lastMouseX > mouseX) {
    theSheep.sheepModel.rotateY(radians(mouseX%(PI*2)));
  } else {
    theSheep.sheepModel.rotateY(-1*radians(mouseX%(PI*2)));
  }


  lastMouseX = mouseX;
}

/*
 * Network server
 */
void pollServer() {
  try {
    Client c = _server.available();
    // append any available bytes to the buffer
    if (c != null) {
      _buf.append(c.readString());
    }
    // process as many lines as we can find in the buffer
    int ix = _buf.indexOf("\n");
    while (ix > -1) {
      String msg = _buf.substring(0, ix);
      msg = msg.trim();
      //println(msg);
      processCommand(msg);
      _buf.delete(0, ix+1);
      ix = _buf.indexOf("\n");
    }
  } 
  catch (Exception e) {
    println("exception handling network command");
    e.printStackTrace();
  }
}

Pattern cmd_pattern = Pattern.compile("^\\s*(p|b|a|f )\\s+(\\d+)\\s+(\\d+),(\\d+),(\\d+)\\s*$");

void processCommand(String cmd) {
  Matcher m = cmd_pattern.matcher(cmd);
  if (!m.find()) {
    println("Input was malformed, please conform to \"[a,p,b] panelId r,g,b\" where a = all sides, b=boring, p= party, panelId = numeric value, r,g, and b are red green and blue values between 0 and 255");
    return;
  }
  String side = m.group(1);
  int panel = Integer.valueOf(m.group(2));
  int r    = Integer.valueOf(m.group(3));
  int g    = Integer.valueOf(m.group(4));
  int b    = Integer.valueOf(m.group(5));

  System.out.println("side:"+side+" "+String.format("panel:%d to r:%d g:%d b:%d", panel, r, g, b));
  
  if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255 ) {
     System.out.println("Bypassing last entry because an r,g,b value was not between 0 and 255:"+r+","+g+","+b); 
     return;
  }

  // modify to read the mapping of panel to polygon.
  //honeycomb.setCellColor(cell, color(r,g,b));  

  theSheep.setPanelColor(side, panel, color(r, g, b));
}

/*
 * Load label mapping file
 */
HashMap<Integer, ArrayList<Integer>> loadPolyMap(String labelFile, String sidePorB) {
  HashMap<Integer, ArrayList<Integer>> polyMap = new HashMap<Integer, ArrayList<Integer>>();  
  Table table = loadTable(labelFile);

  println(table.getRowCount() + " total rows in table"); 

  for (TableRow row : table.rows ()) {
    if (row.getString(4).equals(sidePorB)) {
      ArrayList<Integer> temp = new ArrayList<Integer>();
      int panel = row.getInt(0);

      temp.add(row.getInt(1));
      temp.add(row.getInt(2)); 
      temp.add(row.getInt(3));

      polyMap.put(panel, temp);
    }
  }
  return polyMap;
}

class Sheep {

  PShape sheepModel;
  PShape[] sheepPanelArray;

  public Sheep(String fileName) {
    sheepModel = loadShape(fileName); 
    sheepPanelArray = sheepModel.getChildren();
  }

  void setPanelColor(String side, int panel, color c) {
    ArrayList<Integer> polygons = new ArrayList<Integer>();
    if (side.equals("p") && partySideMap.get(panel) != null) {
      polygons.addAll(partySideMap.get(panel));
    } else if (side.equals("b") && boringSideMap.get(panel) != null) {
      polygons.addAll(boringSideMap.get(panel));
    } else if (side.equals("a")) {
      if (partySideMap.get(panel) != null) {
        polygons.addAll(partySideMap.get(panel));
      }
      if (boringSideMap.get(panel) != null) {
          polygons.addAll(boringSideMap.get(panel));
      }
    } else if (side.equals("f")) {
      Iterator partyItr = partySideMap.keySet().iterator();
      
      while (partyItr.hasNext()) {
         polygons.addAll(partySideMap.get(partyItr.next())); 
      }
      
      Iterator boringItr = boringSideMap.keySet().iterator();
      
      while (boringItr.hasNext()) {
         polygons.addAll(boringSideMap.get(boringItr.next())); 
      }
      
    
    }      

    if (polygons != null && polygons.size() > 0) {
      for (Integer polygon : polygons) {
  
        if (polygon != null && polygon != -1) {
          sheepPanelArray[polygon].disableStyle();
  
          fill(c);
  
          shape(sheepPanelArray[polygon]);
        }
      }
    } else {
       System.out.println("Panel number was not found in map.  Bypassing command."); 
    }
  } // end setPanelColor
}

