#include <iostream>
#include <sys/types.h>
#include <shadow.h>
#include <cstdlib>
#include <unistd.h>
#include <string.h>

using namespace std;

string genSalt(){
    const string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    srand(time(NULL));
    string salt = "$6$";
    for(int i = 3; i < 19; i++){
        int r = rand() % (ALPHABET.length() - 1);
        salt += ALPHABET[r];
    }
    return salt;
}

char* hashPassword(string password){
        char *pass = crypt(password.c_str(), genSalt().c_str());
        return pass;
}

bool checkUserExit(string username){
    spwd *pw = getspnam(username.c_str());
    if(pw == NULL){
        return false;
    }
    return true;
}

bool checkPassword(string oldPassword, string username){
    spwd *pw = getspnam(username.c_str());
    char salt[20];
    for(int i = 0; i< 19; i++){
        salt[i] = pw->sp_pwdp[i];
    }
    salt[19] = '\0';
    if( strcmp( (const char *) pw->sp_pwdp, (const char *) crypt(oldPassword.c_str(), salt) ) != 0){
        return false;
    }
    return true;
}

int changePassword(string newPassword, string username){
    FILE *file;
    spwd *pw;
    if( !(file = fopen(SHADOW, "r+")) ){
        cout << "Mo file /etc/shadow khong thanh cong." << endl;
        return -1;
    }
    while( (pw = getspent()) != NULL){
        if(strcmp(pw->sp_namp, username.c_str()) == 0){
            pw->sp_pwdp = hashPassword(newPassword);
        }
        int res = putspent(pw, file);
        if(res < 0){
            cout << "Co loi xay ra khi ghi file." << endl;
            return -1;
        }
    };
    fclose(file);
    return 0;
}

int main(){
    string username, oldPassword, newPassword;
    cout << "Nhap username: ";
    cin >> username;
    if(!checkUserExit(username)) {
        cout << "User khong ton tai" << endl;
        return 1;
    }
    while(true) {
        cout << "Vui long nhap password: ";
        cin >> oldPassword;
        if(checkPassword(oldPassword, username)) break;
        else cout << "Password sai. ";
    }
    cout << "Nhap password moi: ";
    cin >> newPassword;
    int result = changePassword(newPassword, username);
    if(result == 0){
        cout << "Doi mat khau thanh cong.";
    }
    else{
        cout << "Doi mat khau that bai. Vui long thu lai.";
    }
    return 0;
}

