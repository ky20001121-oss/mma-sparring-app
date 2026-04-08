package p15;

import java.util.ArrayList;

public class Sb {
    public static void main(String []args){

    StringBuilder sb=new StringBuilder();
    for(int i=1;i<=100;i++){

        sb.append(i).append(",");
 }
 String s=sb.toString();
 System.out.println(s);

 String []a=s.split(",");
 
}


}
