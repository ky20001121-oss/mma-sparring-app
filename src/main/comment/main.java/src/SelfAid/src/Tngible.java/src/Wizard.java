public class Wizard {
    private int hp;
    private int mp;
    private String name;
    private Wand wand;

public void setName(String name){

    if (name==null||name.length()<3) {
        System.out.println("名前が短すぎます");
        
    }
    this.name=name;

}  
public void  Wand(Wand wand){

    if (wand ==null) {
        throw new IllegalArgumentException("杖を装備してください");
        
    }
    this.wand=wand;

} 

public void setHp(int hp){

    if (hp<0){
        this.hp=0;
    
    }else{
        this.hp=hp;
    }
}
public void setMp(int mp){

    if (mp<0) {
        throw new IllegalArgumentException("MPは０以上の値を入れてください");

        
    }
}
}

