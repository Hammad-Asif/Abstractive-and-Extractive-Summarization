using System;
using System.Collections.Generic;
using System.Text;
using DAL;
namespace BLL
{
    public class AbstractorBll
    {
        public string getData(string path)
        {
            return new AccessData().getdata(path, "code/Abstract.py",getFile(path));

        }
        private string getFile(string path)
        {
            for (int i = path.Length - 1; i > 0; i--)
            {
                if (path[i] == '\\')
                {
                    return path[i + 1].ToString();
                }
            }
            return null;
        }
    }

}
