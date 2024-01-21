using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

namespace DAL
{
    public class AccessData
    {
        public string getdata(string path,string fileName,string file)
        {
            Process cmdProcess = new Process();
            cmdProcess.StartInfo.FileName = "cmd.exe";
            if (file == null)
            { 
                cmdProcess.StartInfo.Arguments = "/C python " + fileName + " \"" + path + "\""; 
            }
            else
            {
                cmdProcess.StartInfo.Arguments = "/C python " + fileName + " \"" + path + "\" \""+file + "\"";
                
            }
            //return cmdProcess.StartInfo.Arguments;
            cmdProcess.StartInfo.CreateNoWindow = false;
            cmdProcess.StartInfo.WindowStyle = ProcessWindowStyle.Normal;
            cmdProcess.StartInfo.RedirectStandardOutput = true;
            cmdProcess.StartInfo.RedirectStandardInput = false;
            cmdProcess.StartInfo.RedirectStandardError = true;
            cmdProcess.StartInfo.UseShellExecute = false;
            cmdProcess.Start();
            string summary = "";
            
            while (!cmdProcess.StandardOutput.EndOfStream)
            {
                summary += cmdProcess.StandardOutput.ReadLine();
            }
            if(summary=="")
            {
                summary = cmdProcess.StandardError.ReadToEnd();
            }
            cmdProcess.WaitForExit();
            return summary;
        }
    }

}
