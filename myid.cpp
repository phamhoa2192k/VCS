#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <pwd.h>
#include <grp.h>
using namespace std;

int main(){
    int ngroups = 0;
    passwd *pw;
    string username;
    cout << "Vui long nhap username: ";
    cin >> username;
    pw = getpwnam(username.c_str());
    if(pw == NULL){
        cout << "Khong tim thay user tuong ung." << endl;
        return 1;
    }
    cout << "ID: " << pw->pw_uid << endl;
    cout << "Username: " << pw->pw_name << endl;
    cout << "Home folder: " << pw->pw_dir << endl;
    cout << "Cac group cua " << pw->pw_name << ": " << endl;
    getgrouplist(pw->pw_name, pw->pw_gid, NULL, &ngroups);
    __gid_t groups[ngroups];
    getgrouplist(pw->pw_name, pw->pw_gid, groups, &ngroups);
    for (int i = 0; i < ngroups; i++){
        struct group* gr = getgrgid(groups[i]);
        cout << "\t+Group " << i + 1 << ": " << gr->gr_name << endl;
    }
    return 0;
}

