### 景点列表接口

### 请求地址
/sight/sight/list

### 调用方式
GET

### 请求参数
<table>
    <thead>
<tr>
    <th>字段</th>
    <th>必选</th>
    <th>类型</th>
    <th>说明</th>
</tr>
    </thead>
<tbody>
    <tr class="warning">
        <td>is_top</td>
        <td>false</td>
        <td>bool</td>
        <td>是否为精选景点</td>
    </tr>
    <tr class="warning">
        <td>is_hot</td>
        <td>false</td>
        <td>bool</td>
        <td>是否为热门景点</td>
    </tr>
    <tr class="warning">
        <td>page</td>
        <td>false</td>
        <td>int</td>
        <td>分页</td>
    </tr>
</tbody>
</table>

### 返回结果
```
{
	meta: {
		total_count: 10,
		page_count: 2,
		current_page: 1
	},
	objects: [{
			id: 1,
			name: "广州长隆旅游度假区",
			main_img: "/static/home/hot/h2.jpg",
			score: 5,
			province: "广东省",
			city: "广州市",
			comment_count: 0
		},
		{
			id: 10,
			name: "增城白水寨风景名胜区",
			main_img: "/static/home/hot/h9.jpg",
			score: 5,
			province: "广东省",
			city: "增城市",
			comment_count: 0
		},
		{
			id: 9,
			name: "岭南印象园",
			main_img: "/static/home/hot/h8.jpg",
			score: 5,
			province: "广东省",
			city: "广州市",
			comment_count: 0
		},
		{
			id: 8,
			name: "珠江夜游",
			main_img: "/static/home/hot/h10.jpg",
			score: 4.5,
			province: "广东省",
			city: "广州市",
			comment_count: 0
		},
		{
			id: 7,
			name: "广东科学中心",
			main_img: "/static/home/hot/h6.jpg",
			score: 4.5,
			province: "广东省",
			city: "广州市",
			comment_count: 0
		}
	]
}
```

### 返回字段说明
<table>
    <thead>
<tr>
    <th>字段</th>
    <th>类型</th>
    <th>说明</th>
</tr>
    </thead>
<tbody>
    <tr>
        <td>meta</td>
        <td></td>
        <td>分页元数据</td>
    </tr>
    <tr>
        <td>objects</td>
        <td></td>
        <td>景点列表对象，详细如下</td>
    </tr>
    <tr>
        <td>id</td>
        <td>int</td>
        <td>景点id</td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>景点名称</td>
    </tr>
    <tr>
        <td>main_img</td>
        <td>String</td>
        <td>主图url地址</td>
    </tr>
    <tr>
        <td>score</td>
        <td>float</td>
        <td>评分</td>
    </tr>
    <tr>
        <td>province</td>
        <td>String</td>
        <td>省份</td>
    </tr>
    <tr>
        <td>city</td>
        <td>String</td>
        <td>市/区</td>
    </tr>
    <tr>
        <td>comment_count</td>
        <td>int</td>
        <td>评论数量</td>
    </tr>
</tbody>
</table>
