public class Tangible extends Asset implements Things {

    
    private String color;
    private double weight;
   

public Tangible(String name, int price, String color){

    super(name, price);
    this.color=color;
    

} 

@Override
public double getWeight(){return this.weight;}

@Override
public void setWeight(double weight){
    this.weight=weight;
}

public String getColor(){return this.color;}

    
}
