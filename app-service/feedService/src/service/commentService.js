const { SUCCESS } = require("../../../local/en/message");
const mongoose = require("mongoose");
let ObjectId = mongoose.Types.ObjectId;

const add = async (req, res, next) => {
  try {
    let {user} = req.user;
    let data = req.body;
    data.user = user;
    result = await new Models.Comment(data).save();
    return res.send({
      result,
      message: MSG.COMMENT_ADDED,
      status: STATUS_CODE.OK,
    });
  } catch (error) {
    return res.send({
      error: error.message,
      status: STATUS_CODE.INTERNAL_SERVER_ERROR,
    });
  }
};

const getComment = async (req, res, next) => {
  try {
    let { item_id } = req.query;
    item_id = parseInt(item_id);
    let { user: userId } = req.user;
    let pipeline = [
      {
        $match: {
          item_id,
        },
      },
      {
        $lookup: {
          from: "users",
          localField: "user",
          foreignField: "_id",
          as: "userData",
        },
      }, 
      {
        $unwind: { path: "$userData",preserveNullAndEmptyArrays: true  },
      },
      {
        $lookup: {
          from: "commentactivities",
          let: { comment: "$_id" },
          pipeline: [
            {
              $match: {
                $expr: {
                  $and: [
                    {
                      comment: "$$comment",
                    },
                    {
                      $or: [{ like: true }, { view: true }, { dislike: true }],
                    },
                  ],
                },
              },
            },
            {
              $project: {
                like: 1,
                view: 1,
                dislike: 1,
                comment: 1,
                liked: {
                  $cond: [
                    {
                      $and: [
                        { $eq: ["$user", ObjectId(userId)] },
                        { $eq: ["$like", true] },
                      ],
                    },
                    true,
                    false,
                  ],
                },
                disliked: {
                  $cond: [
                    {
                      $and: [
                        { $eq: ["$user", ObjectId(userId)] },
                        { $eq: ["$deslike", true] },
                      ],
                    },
                    true,
                    false,
                  ],
                },
              },
            },
          ],
          as: "activity_data",
        },
      },
      {
        $project: {
          name: "$userData.name",
          profile_photo: "$userData.image",
          parent_id: 1,
          user: 1,
          comment: 1,
          posted_at: 1,
          is_liked: {
            $sum: {
              $size: {
                $filter: {
                  input: "$activity_data",
                  as: "activity",
                  cond: {
                    $and: [
                      { $eq: ["$$activity.like", true] },
                      { $eq: ["$$activity.dislike", false] },
                      { $eq: ["$$activity.comment", "$_id"] },
                    ],
                  },
                },
              },
            },
          },
          is_disliked: {
            $sum: {
              $size: {
                $filter: {
                  input: "$activity_data",
                  as: "activity",
                  cond: {
                    $and: [
                      { $eq: ["$$activity.like", false] },
                      { $eq: ["$$activity.dislike", true] },
                      { $eq: ["$$activity.comment", "$_id"] },
                    ],
                  },
                },
              },
            },
          },
          disliked: {
            $sum: {
              $size: {
                $filter: {
                  input: "$activity_data",
                  as: "activity",
                  cond: {
                    $and: [
                      { $eq: ["$$activity.dislike", true] },
                      {
                        $eq: ["$$activity.like", false],
                      },
                      { $eq: ["$$activity.comment", "$_id"] },
                    ],
                  },
                },
              },
            },
          },
          likes_count: {
            $sum: {
              $size: {
                $filter: {
                  input: "$activity_data",
                  as: "activity",
                  cond: {
                    $and: [
                      { $eq: ["$$activity.like", true] },
                      { $eq: ["$$activity.dislike", false] },
                      { $eq: ["$$activity.comment", "$_id"] },
                    ],
                  },
                },
              },
            },
          },
        },
      },
    ];
    let result = await aggregation(pipeline);
    return res.send({
      data: result,
      message: MSG.DISPLAY_MSG,
      status: STATUS_CODE.OK,
    });
  } catch (error) {
    return res.send({
      error: error.message,
      status: STATUS_CODE.INTERNAL_SERVER_ERROR,
    });
  }
};

const aggregation = async (pipeline) => {
  try {
    return Models.Comment.aggregate(pipeline);
  } catch (error) {
    throw error.message;
  }
};

const getCommentById = async (req, res, next) => {
  try {
    let { id } = req.params;
    let pipeline = [
      {
        $match: {
          parent_id: ObjectId(id),
        },
      },
      {
        $lookup: {
          from: "users",
          localField: "user",
          foreignField: "_id",
          as: "userData",
        },
      },
      {
        $unwind: { path: "$userData" },
      },
      {
        $project: {
          name: "$userData.name",
          profile_photo: "$userData.image",
          parent_id: 1,
          user: 1,
          comment: 1,
          posted_at: 1,
        },
      },
    ];
    let result = await aggregation(pipeline);
    return res.send({
      data: result,
      message: MSG.DISPLAY_COMMENT,
      status: STATUS_CODE.OK,
    });
  } catch (error) {
    return res.send({
      error: error.message,
      status: STATUS_CODE.INTERNAL_SERVER_ERROR,
    });
  }
};

module.exports = {
  add,
  getComment,
  getCommentById,
};
