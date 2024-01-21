using System;
using System.Collections.Generic;
using System.Text;
using DAL;
namespace BLL
{
    public class ExtractorBll
    {
        public string getData(string path)
        {
            return new AccessData().getdata(path, "code/Extract.py",null);
        }
    }
}
