#include <vector>
#define loop(x, n) for (int x = 0; x < n; x++)
#define rloop(x, n) for (int x = n - 1; x >= 0; x--)
#include <fstream>
#include <string>
#include <iostream>
#define contains(s1, s2) (s1.find(s2) != std::string::npos)

using namespace std;

vector<string> pm(5);

bool arrcontains(vector<string> v1, string s1)
{
    bool t = 0;
    loop(x, v1.size()) t |= (contains(s1, v1[x]));
    return t;
}

void iterate(vector<string> &v1, string s1)
{
    v1[0] = s1;
    rloop(x, v1.size()) if (x != 0) v1[x] = v1[x - 1];
}

int main(int argc, char** argv)
{
    cout << argv[1];
    if (argc != 2){
        cout << "Incorrect parameters" << endl;
        return 1;
    }

    string msg = "";
    string pm = "";
    string pm2 = "";
    string pm3 = "";
    string arg1 = argv[1];
    ifstream fin("serverdump/" + arg1 + ".txt");
    ofstream fout("cleaned/" + arg1 + ".txt");

    while (getline(fin, msg))
    {
        //msg=msg.erase (3,15);
        //msg = msg.substr(18);
        if (msg.size() < 2)
            continue;

        // spam filtering    
        if (contains(msg, pm) || contains(msg, pm2) || contains(msg, pm3))
        {
            pm = msg;
            pm2 = pm;
            pm3 = pm2;
            continue;
        }

        //cout<<msg<<endl;
        if(msg.length()>800)continue;
        fout << msg << endl;
        pm = msg;
        pm2 = pm;
        pm3 = pm2;
    }
    // optional
    fin.close();
    fout.close();
    return 0;
}