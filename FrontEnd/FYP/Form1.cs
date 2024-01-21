using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using BLL;
namespace FYP
{
    public partial class Form1 : Form
    {
        string path;
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            path = "";
        }

        private void openFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog fileDialog = new OpenFileDialog();
            fileDialog.Filter = "txt file (*.txt)|*.txt";
            if(fileDialog.ShowDialog()==DialogResult.OK)
            {
                path = fileDialog.FileName;
                readFile();
            }

        }
        private void readFile()
        {
            string data = File.ReadAllText(path);
            txt.Text = data;
            int count = 0;
            count = data.Split('.').Count();
            txt_tb.Text = count.ToString();
        }
        
        private void abstractSummaryToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string sumTxt = "";
            try
            {
                sumTxt = new AbstractorBll().getData(path);
                
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message, "Summary Generator", MessageBoxButtons.OKCancel,MessageBoxIcon.Error );
            }
            summary.Text = sumTxt;
            int count = 0;
            count = sumTxt.Split('.').Count();
            sum_tb.Text = count.ToString();
        }

        private void extractSummaryToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string sumTxt = "";
            sumTxt=extractor();
            summary.Text = sumTxt;
            int count = 0;
            count = sumTxt.Split('.').Count();
            sum_tb.Text = count.ToString();
        }
        private string extractor()
        {
            string sumTxt = "";
            try
            {
                sumTxt = new ExtractorBll().getData(path);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Summary Generator", MessageBoxButtons.OKCancel, MessageBoxIcon.Error);
                return null ;
            }
            return sumTxt;
        }
        private void saveFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog fileDialog = new SaveFileDialog();
            fileDialog.Filter = "Text File |*.txt";
            if(fileDialog.ShowDialog()==DialogResult.OK)
            {
                File.WriteAllText(fileDialog.FileName, summary.Text);
                MessageBox.Show("Summary has been saved", "Summary Generator", MessageBoxButtons.OKCancel, MessageBoxIcon.Information);
            }
        }

        private void quitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }
    }
}
