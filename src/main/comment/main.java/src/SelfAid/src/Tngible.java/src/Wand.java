public class Wand{

    private String name;
    private double power;

public void setNmae(String name){

    if ( name==null||name.length()<3) {

        System.out.println("名前が短すぎます");
        
    }
    this.name=name;

}  

public void setPower(double power){

    if (power<0.5||power>100) {
        System.out.println("数値が範囲外です");
        
    }

    this.power=power;
}

        


}