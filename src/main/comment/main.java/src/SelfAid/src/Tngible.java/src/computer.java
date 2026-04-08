public class computer extends Tangible {
    String makerName;
    
public computer(String name, int price, String color, String makerName){
    super(name, price,color);
    this.makerName=makerName;
}
public String getMakerName(){return this.makerName;}


}
