/*
  Playing around with hex drawing, as described at:
  http://www.redblobgames.com/grids/hexagons/
  
  Grid shapes are described in arrays of arrays:
  {skip_count, fill_count, skip_count ...}
*/

import processing.net.*;
import java.util.regex.*;
Table table;

boolean DRAW_LABELS = true;
//boolean POINTY_TOP = true;
boolean DARK_MODE = false;






// model vars
HexForm honeycomb = null;
HashMap<Integer,String> labels = null;

// network vars
int port = 4444;
Server _server; 
StringBuffer _buf = new StringBuffer();

color defaultHexLine() {
 return color(255,255,255);
}

color defaultHexFill() {
  return color(255,0,255);
}

PVector a = new PVector(400, 100);
PVector b = new PVector(100, 600);
PVector c = new PVector(700, 600);
float hue;
 

void setup() {
  size(5000,5000);
  rotate(radians(0));
  frameRate(30);

  //  println(PFont.list());
  PFont f = createFont("Helvetica", 12, true);
  textFont(f, 12);
  
  labels = loadLabels("mapping_tri.csv");
  
  honeycomb = makeSimpleGrid(8,1,500,300);  
  //honeycomb = makeHexForm(SNOWFLAKE, 50, 50);
  
  _server = new Server(this, port);
  println("server listening:" + _server);
}

void drawCheckbox(int x, int y, boolean checked) {
  int size = 20;
  stroke(0);
  fill(255);  
  rect(x,y,size,size);
  if (checked) {    
    line(x,y,x+size,y+size);
    line(x+size,y,x,y+size);
  }  
}


void drawBottomControls() {
  // draw a bottom white region
  fill(255,255,255);
  rect(0,500,500,50);
  
  // draw checkboxes
  stroke(0);
  fill(255);
  drawCheckbox(20,510, DRAW_LABELS); // label checkbox
 // drawCheckbox(190,510, POINTY_TOP); // pointy-top checkbox
  drawCheckbox(360,510, DARK_MODE); // dark mode
    
  // draw text labels
  fill(0);
  textAlign(LEFT);  
  text("Draw Labels", 50, 525);
  text("Pointy Top", 220, 525);
  text("Dark Mode", 390, 525);
}


void mouseClicked() {  
  //println("click! x:" + mouseX + " y:" + mouseY);
  if (mouseX > 20 && mouseX < 40 && mouseY > 510 && mouseY < 530) {
    // clicked draw labels button
    DRAW_LABELS = !DRAW_LABELS;
  } else if (mouseX > 360 && mouseX < 380 && mouseY > 510 && mouseY < 530) {
    DARK_MODE = !DARK_MODE;
  }  
}

void draw() {
  background(250);
  drawBottomControls();
  honeycomb.draw();
  pollServer();
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
  } catch (Exception e) {
    println("exception handling network command");
    e.printStackTrace();
  }  
}

//Pattern cmd_pattern = Pattern.compile("^\\s*(\\d+)\\s+(\\d+),(\\d+),(\\d+)\\s*$");
Pattern cmd_pattern = Pattern.compile("^\\s*(p|b|a|f )\\s+(\\d+)\\s+(\\d+),(\\d+),(\\d+)\\s*$");

void processCommand(String cmd) {
  Matcher m = cmd_pattern.matcher(cmd);
  if (!m.find()) {
    println("ignoring input!");
    return;
  }
  String side = m.group(1);
  int cell = Integer.valueOf(m.group(2));
  int r    = Integer.valueOf(m.group(3));
  int g    = Integer.valueOf(m.group(4));
  int b    = Integer.valueOf(m.group(5));
  
  honeycomb.setCellColor(cell, color(r,g,b));  
}

/*
mappings* Load label mapping file
 */
HashMap<Integer,String> loadLabels(String labelFile) {
  HashMap<Integer,String> labels = new HashMap<Integer,String>();  
  Table table = loadTable(labelFile);
      
  println(table.getRowCount() + " total rows in table"); 

  for (TableRow row : table.rows()) {
    int id = row.getInt(0);
    String coord = row.getString(1);
    labels.put(id, coord);    
  }
  return labels;
}  




HexForm makeSimpleGrid(int rows, int cols, int start_x, int start_y) {
  HexForm form = new HexForm();
  table = loadTable("/Users/jmajor/projects/pyramidtriangles/Simulators/TriangleSimulator/triangleCellMapping.csv", "header");
  for (TableRow row : table.rows()) {
    String shape = row.getString("shape");
    int x1 = row.getInt("x1");
    int y1 = row.getInt("y1");
    int x2 = row.getInt("x2");
    int y2 = row.getInt("y2");
    int x3 = row.getInt("x3");
    int y3 = row.getInt("y3");
    int id = row.getInt("id");
    //triangle(x1,y1,x2,y2,x3,y3); 
   // print(shape);
    form.add(new Hex(x1,y1,x2,y2,x3,y3,id),id);  
    }
  
  return form;  
}

class HexForm {
  ArrayList<Hex> hexes;
  //HashMap<String,Hex> hexesById;
  
  HexForm() {
    hexes = new ArrayList<Hex>();
    //hexesById = new HashMap<String, Hex>();
  }
  
  void add(Hex h, int hexId) {
//    int hexId = hexes.size();
//    if (labels != null) {
//      h.setId(labels.get(hexId));
//    } else {
//      h.setId(String.valueOf(hexId));
//    }
    print("HEXID:", hexId);
    h.setId(hexId);
    hexes.add(h);
  }
  
  int size() {
    return hexes.size();
  }
  
  void draw() {
    for (Hex h : hexes) {
      h.draw();
    }
  }
  
  // XXX probably need a better API here!
  void setCellColor(int i, color c) {
    if (i >= hexes.size()) {
      println("invalid offset for HexForm.setColor: i only have " + hexes.size() + " hexes");
//      hexes.get(1).setColor(255);

    } else {
      hexes.get(i).setColor(c);
    }
  }
    
}

class Hex {
  int id = 0; // optional
  int x1;
  int y1;
  int x2;
  int y2;
  int x3;
  int y3;
  int cell;
 
  Integer c; // can store color/int or null
  
  Hex(int x1, int y1,int x2, int y2,int x3, int y3, int id) {
    print("CreateHex\n");
    this.x1 = x1;
    this.y1 = y1;
    this.x2 = x2;
    this.y2 = y2;
    this.x3 = x3;
    this.y3 = y3;
    this.c = null;
    this.id = id;
    this.cell = 0;
  }

  void setId(int id) {
    this.id = id;
    print("pass");
  }
  
  void setColor(color c) {
    this.c = c;
  }


  void draw() {
    color fill_color = (this.c != null) ? c : defaultHexFill();  
    fill(fill_color);
    stroke(defaultHexLine());

    beginShape();
    triangle(this.x1,this.y1,this.x2,this.y2,this.x3,this.y3);  
    
    endShape(CLOSE);
    
    // draw text label
    if (DRAW_LABELS && this.id != 0) {
//      fill(defaultHexLine());
//      if (this.cell == 0) {
        fill(defaultHexLine());
         
        if (this.y1 == this.y2) {
          textAlign(CENTER); 
          print(this.id,"pointy");
          text(this.id,this.x1+12,this.y1+10);
        } else {
          textAlign(BOTTOM); 
          print(this.id,"flat");
          text(this.id,this.x1,this.y1+30);
        }
//        this.cell = 1;
//      } else {
//        textAlign(BOTTOM);
//        text(this.id,this.x1+20,this.y3);
//        this.cell = 0;
  //    }
  //    if (this.id % 2 == 0) {
   //     textAlign(CENTER);
    //    text(this.id,this.x1,this.y1);/
//
  //    } else {
    //    textAlign(CENTER);
      //  text(this.id,this.x3+5,this.y3);
//
  //   }

 //     print(this.id, this.x1, this.y2,this.x2, this.y2,this.x3, this.y3 );
    }
    noFill();
    
    
  }
}
