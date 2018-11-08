#include <iostream>
#include <fstream>
#include <cstdio>
#include <sstream>
#include <string>
#include <cstdlib>
#include <vector>
#include <list>
#include <algorithm>
#include <iterator>
#include <map>
using namespace std;

typedef struct FpNode
{
	int frequence;
	int itemName;
	FpNode * parent;
	vector<FpNode *>children;
	FpNode * nextfriend;
	bool operator < (FpNode const & Node) const
	{
		return frequence > Node.frequence;
	}
}node;


typedef struct headItem
{
	int frequence;
	int itemName;
  list<node *> phead;
  headItem(int i,int f){
    itemName = i;
    frequence = f;
  }
}headItem;

bool cmp_headItem(headItem a, headItem b)
{
	if (a.frequence!=b.frequence)
    return a.frequence > b.frequence;
	else
		return a.itemName > b.itemName;
}

struct freItemList
{
	vector<int> item;
	int count;
};

bool compare_item (freItemList a, freItemList b)
{
		if(a.item.size()!=b.item.size())
    	return a.item.size() < b.item.size();
		else{
			int i = 0;
			while(a.item[i] == b.item[i])
				i++;
			return a.item[i] < b.item[i];
		}
}

typedef struct freItem
{
	int frequence;
	int itemName;
  freItem(int i,int f){
    itemName = i;
    frequence = f;
  }
}freItem;

bool cmp_freItem(freItem a, freItem b)
{
		if (a.frequence!=b.frequence)
			return a.frequence > b.frequence;
    else
			return a.itemName > b.itemName;
}


class Fptree {
  public:
    Fptree(double min_s, string tran_file_name, string fp_file_name );
    vector<vector<freItem> > read_file();
		vector<headItem> build_headtable(vector<vector<freItem> > transactions);
    vector<vector<freItem> > build_ordered_transactions(vector<headItem> headtable, vector<vector<freItem> > transactions);
    void createFpTree(vector<headItem> & headtable, vector<vector<freItem> > ordered_transactions);
		vector<vector<freItem> > getFrequentModeBase(list<node *>  const phead);
		void generateFrequentItems(vector<headItem>& headerTable, vector<int> base, list<freItemList>& modeLists);
		void writeFile(list<freItemList> itemList);

  private:
    double min_s;
    string tran_file_name;
    string fp_file_name;
		int transaction_num;
    // vector<vector<int> > transactions;
    // map<int, int> item_frquency_map;
    // vector<vector<frequent_item> > ordered_transactions;
    // vector<frequent_item> headtable;
    // node* headerNode;
		int findPosInheaderTable(vector<headItem> headtable, int it);
    int findPosInChildren(int item, vector<node*>const & children);
};


Fptree::Fptree(double min_s, string tran_file_name, string fp_file_name ){
  this->min_s = min_s;
  this->tran_file_name = tran_file_name;
  this->fp_file_name = fp_file_name;

  // printf("%f %s %s\n", this->min_s, this->tran_file_name.c_str(), \
  //         this->fp_file_name.c_str());
  return;
}

vector<vector<freItem> > Fptree::read_file(){
	vector<vector<freItem> > transactions;
	string line;
  ifstream fin(tran_file_name.c_str());
  if(!fin) {
     cout << "Cannot open input file.\n";
     return (transactions);
  }
  while(!getline(fin, line).eof()){
    vector<freItem> single_tr;
    istringstream ssline(line);
    string number;
    while(getline(ssline, number, ','))
      single_tr.push_back(freItem(atoi(number.c_str()),1));
    transactions.push_back(single_tr);
  }
	transaction_num = transactions.size();
	cout << transaction_num << endl;
  // cout << transactions.size() << endl;
  // for (int i = 0; i < 10; i++){
  //   for (int j = 0; j < transactions[i].size(); j++){
  //     cout << transactions[i][j] << "," ;
  //   }
  //   cout << endl;
  // }
	return (transactions);
}



vector<headItem> Fptree::build_headtable(vector<vector<freItem> > transactions){
  vector<vector<int> > val_and_id;
	vector<headItem> headtable;

  val_and_id.resize(100);
  for (int i = 0; i < 100; i++) {
    val_and_id[i].resize(2); // one to store value, the other for index.
    val_and_id[i][0] = 0;
    val_and_id[i][1] = i;
  }
  for (int i = 0; i < transactions.size(); i++){
    for (int j = 0; j < transactions[i].size(); j++){
      val_and_id[ transactions[i][j].itemName ][0] += transactions[i][j].frequence;
    }
  }
  sort(val_and_id.begin(), val_and_id.end());
  reverse(val_and_id.begin(), val_and_id.end());
  for (int i = 0; i < 100; i++){
    if (val_and_id[i][0] >= min_s * transaction_num){
    }
    else{
      val_and_id.erase( val_and_id.begin()+i, val_and_id.end() );
      break;
    }
  }

  // cout << "Single frequent item numbers : " << val_and_id.size() << endl;
  for (int i=0;i<val_and_id.size();i++){
    // item_frquency_map.insert(pair<int, int>(val_and_id[i][1], val_and_id[i][0]));
    headtable.push_back(headItem(val_and_id[i][1], val_and_id[i][0]));
		// cout << headtable[i].itemName << " : " << headtable[i].frequence << endl;
    headtable[i].phead.clear();
  }
  // vector<PAIR> item_frquency_vec(item_frquency_map.begin(), item_frquency_map.end());
  // sort(item_frquency_vec.begin(), item_frquency_vec.end(), cmp_map);
  // cout << "\nFrequent item list" << endl;
  // for (int i = 0; i != item_frquency_vec.size(); ++i) {
  //   cout << item_frquency_vec[i].first << " : " << item_frquency_vec[i].second << endl;
  // }
	return (headtable);
}


vector<vector<freItem> > Fptree::build_ordered_transactions(vector<headItem> headtable, vector<vector<freItem> > transactions){
	vector<vector<freItem> > ordered_transactions;
	for (int i=0;i<transactions.size();i++){
    vector<freItem> single_row_item;
    for (int j=0;j<transactions[i].size();j++){
			int pos = findPosInheaderTable(headtable, transactions[i][j].itemName);
      if(pos != -1){
        int it = transactions[i][j].itemName;
        int fr = headtable[pos].frequence;
        single_row_item.push_back(freItem(it, fr));
      }
    }
    if (single_row_item.size()> 1){
      sort(single_row_item.begin(),single_row_item.end(), cmp_freItem);
			for (int i = 0; i< single_row_item.size(); i++){
				single_row_item[i].frequence = 1;
			}
      ordered_transactions.push_back(single_row_item);
    }
  }
  // cout << "\nOrdered list" << endl;
  // for (int i=0;i<ordered_transactions.size();i++){
  //   for (int j=0;j<ordered_transactions[i].size();j++){
  //     cout << ordered_transactions[i][j].itemName << ",";
  //   }
  //   cout << endl;
  // }
	return (ordered_transactions);
}

int Fptree::findPosInheaderTable(vector<headItem> headtable, int it){
	int pos = -1;
	for (int p = 0; p != headtable.size(); p++)
	{
		if (headtable[p].itemName == it)
		{
			pos = p;
		}
	}
	return pos;
}


int Fptree::findPosInChildren(int item, vector<node*>const & children){
	int pos = -1;
	for (int i = 0; i < children.size(); i++)
	{
		if (children[i]->itemName == item)
		{
			pos = i;
		}
	}
	return pos;
}

void Fptree::createFpTree(vector<headItem> & headtable,vector<vector<freItem> > ordered_transactions){
  node* headerNode = new node;
  headerNode->itemName = -1;
  headerNode->nextfriend = NULL;
	headerNode->parent = NULL;
	headerNode->frequence = 0;
	headerNode->children.clear();
  for (int i = 0; i< ordered_transactions.size();i++){
    // cout << "Start " << i << endl;
    node* nodeInfp = headerNode;
    int j = 0;
    while(j != ordered_transactions[i].size()){
      int pos = findPosInChildren(ordered_transactions[i][j].itemName, nodeInfp->children);
      if (pos != -1){
        nodeInfp->children[pos]->frequence += ordered_transactions[i][j].frequence;
        nodeInfp = nodeInfp->children[pos];
        j++;
      }
      else{
        while (j!=ordered_transactions[i].size()){
          node* new_node = new node;
          new_node->itemName = ordered_transactions[i][j].itemName;
					new_node->frequence = ordered_transactions[i][j].frequence;
          int pos_h = findPosInheaderTable(headtable, new_node->itemName);
          if (pos_h != -1){
            headtable[pos_h].phead.push_back(new_node);
          }
          nodeInfp->children.push_back(new_node);
          new_node->parent = nodeInfp;
          nodeInfp = new_node;
          j++;
        }
        break;
      }
    }
    // cout << "Finish " << i << endl;
  }
	// cout << "Finish FPtree"  << endl;
	// //
	// node* iter_node;
	// for (int i = 0; i < headtable.size(); i++){
	// 	cout << "Frequent item: "<< headtable[i].itemName << endl ;
	// 	for (auto p = headtable[i].phead.begin(); p != headtable[i].phead.end(); p++){
	// 		iter_node = *p;
	// 		while(iter_node->parent != NULL){
	// 			cout << iter_node->itemName << ":" << iter_node->frequence << ",";
	// 			iter_node = iter_node->parent;
	// 		}
	// 		cout << endl;
	// 	}
	// }


}
//
vector<vector<freItem> > Fptree::getFrequentModeBase(list<node *>  phead)
{
	vector<vector<freItem> > frequentModes;
	// list<node*>::iterator p;
	node * ptr;
	for (auto p = phead.begin(); p != phead.end(); p++)
	{
		vector<freItem> frequentMode;
		ptr = *p;
		int currentFrequency = ptr->frequence;
		//由ptr指针逆行寻找父亲节点
		while (ptr->parent != NULL)
		{
			if (ptr->parent->itemName != -1)
			{
				node temp = *(ptr->parent);
				freItem item(temp.itemName,currentFrequency);
				frequentMode.push_back(item);
				ptr = ptr->parent;
			}
			else{
				break;
			}
		}
		reverse(frequentMode.begin(), frequentMode.end());
		frequentModes.push_back(frequentMode);
	}
	// cout << "Frequent modes" << endl;
	// for (int i = 0; i<frequentModes.size(); i++){
	// 	for (int j = 0; j<frequentModes[i].size(); j++){
	// 		cout << frequentModes[i][j].itemName << ":"<<frequentModes[i][j].frequence <<",";
	// 	}
	// 	cout << endl;
	// }
	return frequentModes;
}
//
//
void Fptree::generateFrequentItems(vector<headItem>& headerTable, vector<int> base, list<freItemList>& modeLists)
{
	if (headerTable.empty())
	{
		// cout << "Finish dipping" << endl;
		return;
	}
	for (int i = 0; i < headerTable.size(); i++)
	{
		/*对于headerTable中的每一项*/
		headItem head_item = headerTable[i];
		freItemList model;
		vector<int> modelbase= base;
		modelbase.push_back(head_item.itemName);
		model.item = modelbase;
		model.count = head_item.frequence;
		modeLists.push_back(model);
		//产生currentMode的条件模式基

		// cout << headerTable[i].itemName << " " << headerTable[i].frequence << " "<< "Phead size: "<< headerTable[i].phead.size() << endl;
		vector<vector<freItem> > ConditionalmodeBase = getFrequentModeBase(headerTable[i].phead);
		//根据条件模式基，生成新的HeaderTable和Fp-tree
		vector<headItem> headerTable2 = build_headtable(ConditionalmodeBase);
		// ConditionalmodeBase =  build_ordered_transactions(headerTable2, ConditionalmodeBase);
		createFpTree(headerTable2, ConditionalmodeBase);
		generateFrequentItems(headerTable2, model.item, modeLists);
	}
}


void Fptree::writeFile(list<freItemList> itemList){
	FILE *fp;
	fp = fopen (fp_file_name.c_str(),"w");
	for (auto i = itemList.begin(); i != itemList.end(); i++){
		for (int j = 0; j < i->item.size()-1; j++){
			fprintf(fp,"%d,",i->item[j]);
		}
		fprintf(fp,"%d:",i->item[i->item.size()-1]);
		double f = double(i->count)/transaction_num;
		// int int_f = f *10000 + 0.5;
		// f = double(int_f)/10000;
		f = (int)(f * 10000 + 0.55)/(10000*1.0);
		fprintf(fp,"%.4f\n",f);
	}
	fclose(fp);
}

int main(int argc, char **argv){
  string tran_file_name;
  string fp_file_name;
  double min_s;
  if (argc == 4 ){
    min_s = atof(argv[1]);
    tran_file_name = string(argv[2]);
    fp_file_name = string(argv[3]);
  }
  else{
    printf("Enter wrong command\n");
    return 0;
  }
  Fptree fptree(min_s, tran_file_name, fp_file_name);
  vector<vector<freItem> > transactions = fptree.read_file();
  vector<headItem> headtable = fptree.build_headtable(transactions);
  vector<vector<freItem> > ordered_transactions = \
		fptree.build_ordered_transactions(headtable, transactions);
  fptree.createFpTree(headtable, ordered_transactions);
	list<freItemList> itemList;//保存频繁项
	vector<int> empty_item;
	fptree.generateFrequentItems(headtable, empty_item, itemList);
	for (auto i = itemList.begin(); i != itemList.end(); i++){
		sort(i->item.begin(),i->item.end());
		// for (int j = 0; j < i->item.size(); j++){
		// 	cout << i->item[j] << ",";
		// }
		// cout << "Frequency:" << i->count ;
		// cout << endl;
	}
	itemList.sort(compare_item);
	// for (auto i = itemList.begin(); i != itemList.end(); i++){
	// 	for (int j = 0; j < i->item.size(); j++){
	// 		cout << i->item[j] << ",";
	// 	}
	// 	cout << "Frequency:" << i->count ;
	// 	cout << endl;
	// }
	cout << itemList.size() << endl;
	fptree.writeFile(itemList);
	return 0;
}
