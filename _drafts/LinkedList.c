#include <stdio.h>
#include <stdlib.h> // malloc
#include <stdbool.h> //bool


struct LL_Node;
struct LinkedList;
struct T_Node;

/* START LL_Node */
typedef struct LL_Node
{
	struct LL_Node* prev;
	struct LL_Node* next;
	int value;
} LL_Node;

LL_Node* LL_Node_init(int value)
{
	LL_Node* node = (LL_Node*)malloc(sizeof(LL_Node));
	node->prev = NULL;
	node->next = NULL;
	node->value = value;
	return node;
}

void LL_Node_print_int(LL_Node* node)
{
	printf("%d ", node->value);
}

void LL_Node_inc_int(LL_Node* node)
{
	node->value++;
}
/* END LL_Node */

/* START LinkedList */
typedef struct LinkedList
{
	struct LL_Node* first;
	struct LL_Node* last;
} LinkedList;

LinkedList* LinkedList_init(LL_Node* node)
{
	LinkedList* linked_list = (LinkedList*)malloc(sizeof(LinkedList));
	linked_list->first = node;
	linked_list->last = node;
	return linked_list;
}

void LinkedList_free(LinkedList* linked_list)
{
	/* TODO: check if this works */
	/* could use LinkedList_popback() here */
	for (LL_Node* node = linked_list->first; node != NULL; /* next condition handled in loop */)
	{
		LL_Node* next_node = node->next;
		free(node);
		node = next_node;
	}
	free(linked_list);
}

LL_Node* LinkedList_add(LinkedList* linked_list, LL_Node* node)
{
	linked_list->last->next = node;
	node->prev = linked_list->last;
	linked_list->last = node;
	return node;
}

/* map a function of type LL_Node* -> void to each element */
void LinkedList_map(LinkedList* linked_list, void(*fn_ptr)(LL_Node*))
{
	for (LL_Node* node = linked_list->first; node != linked_list->last; node = node->next)
	{
		(*fn_ptr)(node);
	}
	(*fn_ptr)(linked_list->last);
}

LL_Node* LinkedList_pop_front(LinkedList* linked_list)
{
	LL_Node* node = linked_list->first;
	linked_list->first = node->next;
	return node;
}

LL_Node* LinkedList_pop_back(LinkedList* linked_list)
{
	LL_Node* node = linked_list->last;
	linked_list->last = node->prev;
	return node;
}

bool LinkedList_is_empty(LinkedList* linked_list)
{
	return linked_list->first == NULL && linked_list->last == NULL;
}

/* END LinkedList */

int main()
{
	LL_Node* node = LL_Node_init(1);
	LinkedList* linked_list = LinkedList_init(node);
	LinkedList_add(linked_list, LL_Node_init(2));
	LinkedList_add(linked_list, LL_Node_init(4));

	// Higher order function time!
	LinkedList_map(linked_list, &LL_Node_print_int);
	printf("\n");
	LinkedList_map(linked_list, &LL_Node_inc_int);
	LinkedList_map(linked_list, &LL_Node_print_int);
	printf("\n");
	LinkedList_free(linked_list);
#ifdef _WIN32
	system("Pause");
#endif
}

