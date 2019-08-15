/*
  Playing around with hex drawing, as described at:
  http://www.redblobgames.com/grids/hexagons/

  Grid shapes are described in arrays of arrays:
  {skip_count, fill_count, skip_count ...}
*/

import processing.net.*;
import java.util.regex.*;

boolean DRAW_LABELS = true;

// model vars
TriangleForm grid = null;

// network vars
int port = 4444;
Server _server; 
StringBuffer _buf = new StringBuffer();

color defaultLineColor = color(255, 255, 255);
color defaultFillColor = color(255, 0, 255);

void setup() {
  size(800,700);
  rotate(radians(0));
  frameRate(30);

  PFont f = createFont("Helvetica", 12, true);
  textFont(f, 12);
  
  grid = makeSimpleGrid();
  
  _server = new Server(this, port);
  println("server listening:" + _server);
}

void drawCheckbox(int x, int y, boolean checked) {
  int size = 20;
  stroke(0);
  fill(255);  
  rect(x, y, size, size);
  if (checked) {    
    line(x, y, x+size, y+size);
    line(x+size, y, x, y+size);
  }  
}

void drawBottomControls() {
  // draw a bottom white region
  fill(255, 255, 255);
  rect(0, 500, 500, 50);

  // draw checkboxes
  stroke(0);
  fill(255);
  drawCheckbox(20, 510, DRAW_LABELS); // label checkbox

  // draw text labels
  fill(0);
  textAlign(LEFT);  
  text("Draw Labels", 50, 525);
}

void mouseClicked() {  
  if (mouseX > 20 && mouseX < 40 && mouseY > 510 && mouseY < 530) {
    // clicked draw labels button
    DRAW_LABELS = !DRAW_LABELS;
  }  
}

void draw() {
  background(250);
  drawBottomControls();
  grid.draw();
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
      processCommand(msg);
      _buf.delete(0, ix+1);
      ix = _buf.indexOf("\n");
    }
  } catch (Exception e) {
    println("exception handling network command");
    e.printStackTrace();
  }  
}

Pattern cmd_pattern = Pattern.compile("^\\s*(\\d+)\\s+(\\d+),(\\d+),(\\d+)\\s*$");

void processCommand(String cmd) {
  Matcher m = cmd_pattern.matcher(cmd);
  if (!m.find()) {
    println("ignoring input!");
    return;
  }
  int cell = Integer.valueOf(m.group(1));
  int r    = Integer.valueOf(m.group(2));
  int g    = Integer.valueOf(m.group(3));
  int b    = Integer.valueOf(m.group(4));
  
  grid.setCellColor(cell, color(r,g,b));
}

TriangleForm makeSimpleGrid() {
  TriangleForm form = new TriangleForm();
  Table table = loadTable("triangleCellMapping.csv", "header");
  for (TableRow row : table.rows()) {
    String shape = row.getString("shape");
    int x1 = row.getInt("x1");
    int y1 = row.getInt("y1");
    int x2 = row.getInt("x2");
    int y2 = row.getInt("y2");
    int x3 = row.getInt("x3");
    int y3 = row.getInt("y3");
    int id = row.getInt("id");
    form.add(new Triangle(x1, y1, x2, y2, x3, y3, id), id);  
  }
  
  return form;  
}

class TriangleForm {
  ArrayList<Triangle> triangles = new ArrayList<Triangle>();

  TriangleForm() {
  }

  void add(Triangle triangle, int id) {
    print("Triangle ID:", id);
    triangle.setId(id);
    triangles.add(triangle);
  }

  int size() {
    return triangles.size();
  }

  void draw() {
    for (Triangle triangle : triangles) {
      triangle.draw();
    }
  }

  // XXX probably need a better API here!
  void setCellColor(int i, color c) {
    if (i >= triangles.size()) {
      println("invalid offset for HexForm.setColor: i only have " + triangles.size() + " hexes");
      return;
    }

    triangles.get(i).setColor(c);
  }
    
}

class Triangle {
  int id = 0; // optional
  int x1;
  int y1;
  int x2;
  int y2;
  int x3;
  int y3;
  int cell;
 
  Integer c; // can store color/int or null
  
  Triangle(int x1, int y1,int x2, int y2,int x3, int y3, int id) {
    print("CreateTriangle\n");
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
    color fill_color = (this.c != null) ? c : defaultFillColor;
    fill(fill_color);
    stroke(defaultLineColor);

    beginShape();
    triangle(this.x1, this.y1, this.x2, this.y2, this.x3, this.y3);

    endShape(CLOSE);

    // draw text label
    if (DRAW_LABELS && this.id != 0) {
        fill(defaultLineColor);

        if (this.y1 == this.y2) {
          textAlign(CENTER); 
          print(this.id,"pointy");
          text(this.id,this.x1+12,this.y1+10);
        } else {
          textAlign(BOTTOM); 
          print(this.id,"flat");
          text(this.id,this.x1,this.y1+30);
        }
    }

    noFill();
  }
}
