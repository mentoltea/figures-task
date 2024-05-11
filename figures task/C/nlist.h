#ifndef C_LIST_NODE
#define C_LIST_NODE

#include <stdlib.h>
#include <stdio.h>


typedef enum {
    false=0,
    true=1
} bool;


//#define List(a) List_struct_##type {a, 1, NULL}

#define LIST_DEF(type)\
	LIST_STRUCT_DEF(type)\
	LIST_FINDELEM_DEF(type)\
    LIST_APPEND_DEF(type)\
    LIST_REPLACE_DEF(type)\
    LIST_DELETE_DEF(type)\
    LIST_POP_DEF(type)\
    LIST_LEN_DEF(type)\
    LIST_SHORT_CREATION(type)\
    LIST_DESTROY_DEF(type)\
    LIST_IN_DEF(type)\
    LIST_REVERSE_DEF(type)\
    LIST_UNIT_DEF(type)\
    LIST_COPY_DEF(type)


#define LIST_STRUCT_DEF(type)\
	typedef struct List_struct_##type list_##type;\
	struct List_struct_##type {\
		type val;\
		size_t length;\
		list_##type *next;\
	};\


#define LIST_FINDELEM_DEF(type)\
	type find_##type(list_##type *list, size_t index) {\
		if (index > list->length - 1) {return;}\
		list_##type *ptr = list;\
		for (int i=0; i < list->length; i++) {\
			if (i==index) { return ptr->val; }\
            if (ptr->next==NULL) {return;}\
			ptr = ptr->next;\
		}\
	}

#define LIST_APPEND_DEF(type)\
	void append_##type(list_##type *list, type elem) {\
		list_##type *ptr = list;\
		list_##type *new_node = (list_##type*)malloc(sizeof(list_##type));\
        new_node->val=elem; new_node->length=NULL; new_node->next=NULL;\
		while (ptr->next != NULL) {\
            ptr = ptr->next;\
		}\
        ptr->next = new_node;\
		list->length += 1;\
    }
		
#define LIST_REPLACE_DEF(type)\
    void replace_##type(list_##type *list, size_t index, type elem) {\
        if (index > list->length-1) {return;}\
        list_##type *ptr = list;\
        for (int i = 0; i<index; i++) {\
            ptr = ptr->next;\
        }\
        ptr->val = elem;\
    }

#define LIST_DELETE_DEF(type)\
    void delete_##type(list_##type *list, size_t index) {\
        if (index > list->length-1) {return;}\
        list_##type *ptr = list;\
        list_##type *last = list;\
        for (int i=0; i<index; i++) {\
            last = ptr;\
            ptr = ptr->next;\
        }\
        last->next=ptr->next;\
        list->length -= 1;\
        free(ptr);\
    }\

#define LIST_POP_DEF(type)\
    void pop_##type(list_##type *list) {\
        if (list->length == 1) { free(list); return;}\
        size_t index = list->length-1;\
        list_##type *ptr = list;\
        for (int i=0; i<index-1; i++) {\
            ptr = ptr->next;\
        }\
        free(ptr->next);\
        ptr->next = NULL;\
        list->length -= 1;\
    }

#define LIST_LEN_DEF(type)\
    size_t len_##type(list_##type *list) {\
        size_t len = 0;\
        list_##type *ptr = list;\
        while (ptr != NULL) {\
            len++;\
            ptr = ptr->next;\
        }\
        list->length = len;\
        return len;\
    }

#define LIST_SHORT_CREATION(type)\
    list_##type* new_##type(type value) {\
        list_##type *list_ptr = (list_##type*)malloc(sizeof(list_##type));\
        list_ptr->val = value; list_ptr->length = 1; list_ptr->next = NULL;\
        return list_ptr;\
    }


#define LIST_DESTROY_DEF(type)\
    void destroy_##type(list_##type *list) {\
        if (!list) {return;}\
        while (list->length > 1) {\
            pop_##type(list);\
        }\
    }


#define LIST_IN_DEF(type)\
    bool in_##type(list_##type *list, type value, bool (*eq)(type, type)) {\
        list_##type *ptr = list;\
        while (ptr->next != NULL) {\
            if (eq(ptr->val, value) == true) {\
                return true;\
            }\
            ptr = ptr->next;\
        }\
        return eq(ptr->val, value);\
    }

#define LIST_REVERSE_DEF(type)\
    void reverse_##type(list_##type *list) {\
        type temp;\
        size_t n = list->length;\
        for (int i=0; i< n/2; i++) {\
            temp = find_##type(list, i);\
            replace_##type(list, i, find_##type(list, n-1-i));\
            replace_##type(list, n-1-i, temp);\
        }\
    }

#define LIST_UNIT_DEF(type)\
    void unit_##type(list_##type *list1, list_##type *list2){\
        list_##type *ptr = list1;\
        while (ptr->next != NULL) {\
            ptr = ptr->next;\
        }\
        ptr->next = list2;\
        list1->length += list2->length;\
    }

#define LIST_COPY_DEF(type)\
    list_##type *list_copy_##type(list_##type *list) {\
        if (!list) {return list;}\
        list_##type *res = new_##type(list->val);\
        list_##type *ptr = list->next;\
        while (ptr != NULL) {\
            append_##type(res, ptr->val);\
            ptr = ptr->next;\
        }\
        return res;\
    }

#endif
