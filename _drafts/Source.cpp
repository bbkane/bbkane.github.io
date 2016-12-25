#include <iostream>
#include <vector>
#include <memory>
#include <string>
#include <queue>
#include <stack>

template <typename DataType>
auto next(std::queue<DataType*>& q)
{
	return q.front();
}

template <typename DataType>
auto next(std::stack<DataType*>& s)
{
	return s.top();
}

template <typename DataType>
struct TreeNode
{
	DataType data_;
	std::vector<std::unique_ptr<TreeNode>> children_;

	TreeNode(DataType data)
		: data_(data)
	{}

	std::string to_string(std::string prepend=" ", int times=0)
	{
		std::string indent = "";
		for (int i = 0; i < times; ++i)
		{
			indent += prepend;
		}
		std::string base = indent + std::to_string(data_);
		for (const auto& c : children_)
		{
			base += "\n";
			base += c->to_string(prepend, times + 1);
		}
		return base;
	}

	//NOTE: the pointer this function returns must not be reassigned or deleted;
	// and it's valididy is tied to the lifetime of the tree
	TreeNode* add_child(DataType data)
	{
		auto child = std::make_unique<TreeNode>(data);
		auto child_p = child.get();
		children_.push_back(std::move(child));
		return child_p;
	}

	void traverse()
	{
		std::stack<TreeNode*> list;
		list.push(this);
		while (!list.empty())
		{
			auto t = next(list);
			list.pop(); // TODO: is t still valid after this? It returns a reference, so i guess it is.
			std::cout << "traversing: " << t->data_ << std::endl;
			for (const auto& i : t->children_)
			{	
				std::cout << "adding: " << i->data_ << std::endl;
				list.push(i.get());
			}
		}
	}
};

int main()
{
	using Tree = TreeNode<int>;

	auto root = Tree(1);
	auto root1 = root.add_child(11);
	auto root2 = root.add_child(12);
	auto root11 = root1->add_child(111);
	std::cout << root.to_string() << std::endl;

	std::cout << "Traversing..." << std::endl;
	root.traverse();
	
#ifdef _WIN32
	system("pause");
#endif // _WIN32
}