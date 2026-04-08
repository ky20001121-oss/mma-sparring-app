package p14;
public class Main {
    public static void main(String[]args){

        Bankaccount a=new Bankaccount("4649",1592);
        Bankaccount b=new Bankaccount("  4649", 0);
      

        if (a.equals(b)) {

            System.out.println("trimメソッドのおかげで、同一の数字とみなされました。");
            
        }else{

            System.out.println("失敗");
        }
        


    }
}
